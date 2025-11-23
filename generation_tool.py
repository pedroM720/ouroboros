import re
from typing import List, Tuple
from spoon_ai.tools.base import BaseTool
from spoon_ai.chat import ChatBot
import os
import subprocess
import sys

from tool_generation_agent import ToolGenerationAgent

def _strip_code_fences(code: str) -> str:
    s = code.strip()
    if s.startswith("```"):
        s = s.removeprefix("```")
    if s.lower().startswith("python"):
        s = s[len("python"):]
    if s.endswith("```"):
        s = s[: -len("```")]
    return s.strip()

def _extract_imports_and_body(code: str) -> Tuple[List[str], str]:
    lines = code.splitlines()
    imports: List[str] = []
    body_lines: List[str] = []
    seen = set()
    imp_re = re.compile(r"^\s*(import\s+.+|from\s+\S+\s+import\s+.+)")
    for line in lines:
        m = imp_re.match(line)
        if m:
            k = m.group(1).strip()
            if k not in seen:
                imports.append(line.strip())
                seen.add(k)
        else:
            body_lines.append(line)
    body = "\n".join(body_lines).strip()
    return imports, body

def _extract_latest_step_code(text: str) -> str:
    step_iter = list(re.finditer(r"(?is)\bStep\s*\d+\s*:", text))
    if step_iter:
        last = step_iter[-1]
        tail = text[last.end():]
    else:
        tail = text
    blocks = re.findall(r"```(?:python\s*)?([\s\S]*?)```", tail)
    if blocks:
        return blocks[-1].strip()
    return tail.strip()

def install_package(package):
    """
    Installs a Python package dynamically using pip via subprocess.
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}: {e}")


name: str = "generation_tool"
description: str = "Generates a tool class file from a description. This should be used for any complex tasks that an LLM may not have reliable accuracy on, or things that require external APIs or arbitrary code execution."
parameters: dict = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "The name of the function. Distinct from class_name."},
            "description": {"type": "string", "description": "Natural language description. Example: A tool that shuffles a string."},
            "inputs": {"type": "string", "description": "Comma separated list of inputs and types. Example: query: str, api-token: str"},
            "outputs": {"type": "string", "description": "Comma separated list of outputs and types. Example: name: str, id: str"},
            "class_name": {"type": "string", "description": "Generated tool class name."}
    },
    "required": ["name", "description", "inputs", "outputs", "class_name"]
}
class GenerationTool(BaseTool):
    agent: ToolGenerationAgent = None

    def __init__(self, llm: ChatBot):
        super().__init__(name=name, description=description, parameters=parameters)
        self.agent = ToolGenerationAgent(llm)

    async def _generate_code(self, spec: str) -> str:
        return await self.agent.run(spec)

    async def execute(self, name: str, description: str, inputs: str, outputs: str, class_name: str = "GeneratedTaskTool") -> str:
        print(f"Attempting to generate {class_name}.")
        print(f"name: \"{name}\", description: \"{description}\", inputs: \"{inputs}\", outputs: \"{outputs}\"")

        raw = await self._generate_code(f"name: \"{name}\", description: \"{description}\", inputs: \"{inputs}\", outputs: \"{outputs}\"")
        latest = _extract_latest_step_code(raw)
        cleaned = _strip_code_fences(latest)
        imports, body = _extract_imports_and_body(cleaned)
        header = ["from spoon_ai.tools.base import BaseTool"] + imports
        assembled_parts = []
        assembled_parts.append("\n".join(header).strip())
        if body:
            assembled_parts.append("\n" + body + "\n")
        # Parse inputs into JSON schema properties
        properties = {}
        required = []
        exec_params = []
        if inputs.strip():
            for inp in inputs.split(","):
                inp = inp.strip()
                if ":" in inp:
                    varName, typ = inp.split(":", 1)
                    varName = varName.strip()
                    typ = typ.strip()
                    json_type = "string"
                    if typ in ("int", "float"):
                        json_type = "number"
                    elif typ == "bool":
                        json_type = "boolean"
                    elif typ == "list":
                        json_type = "array"
                    properties[varName] = {"type": json_type, "description": f"{varName}"}
                    required.append(varName)
                    exec_params.append(varName)

        tool_class = (
            f"class {class_name}(BaseTool):\n"
            f"    name: str = \"{name}\"\n"
            f"    description: str = {repr(description)}\n"
            f"    parameters: dict = {{\n"
            f"        \"type\": \"object\",\n"
            f"        \"properties\": {{\n"
            + "".join([f"            \"{k}\": {repr(v)},\n" for k, v in properties.items()]).rstrip(",\n") + "\n"
            f"        }},\n"
            f"        \"required\": {required}\n"
            f"    }}\n"
            f"    async def execute(self, {', '.join(exec_params)}) -> str:\n"
            f"        return await run({', '.join(exec_params)})\n"
        )

        assembled_parts.append(tool_class)
        final_code = "\n".join(assembled_parts)
        
        try:
            compile(final_code, "<string>", "exec")
        except SyntaxError as e:
            print(f"SyntaxError: {e.msg}")
            print(f"Line: {e.lineno}")
            print(f"Problem: {e.text}")
            return "Failed to generate code. Try again, or if this fails consistently, this may not be possible."

        for module in imports:
            module = module.removeprefix("import ")
            module = module.removeprefix("from ")

            split = module.split(" ")
            split = split[0].split(".")
            install_package(split[0])

        out_dir = os.path.join(os.getcwd(), "generated-tools")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{class_name}.py")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_code)

        return f"Successfully generated tool with name {name}"
        
