import re
from typing import List, Tuple
from spoon_ai.tools.base import BaseTool
from spoon_ai.chat import ChatBot
import os
import subprocess
import sys

from spoon_ai.tools.tool_manager import ToolManager

from dynamic_tool_loader import load_tool
from tool_generation_agent import ToolGenerationAgent
from tool_review_agent import RetoolAgent

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

def parse_packages(final_code):
    for line in final_code.splitlines():
        line = line.strip()
        if line.startswith("# install modules:"):
            line = line.removeprefix("# install modules:").strip()
            for module in line.split(" "):
                install_package(module)

def gen_code(raw, inputs, class_name, name):
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
    return final_code

def tool_path(class_name: str, out_dir):
    return os.path.join(out_dir, f"{class_name}.py")

name: str = "generation_tool"
description: str = "Generates a tool class file from a description. This should be used for any complex tasks that an LLM may not have reliable accuracy on, or things that require external APIs or arbitrary code execution."
parameters: dict = {
    "type": "object",
    "properties": {
            "name": {"type": "string", "description": "The name of the function. Distinct from class_name."},
            "description": {"type": "string", "description": "Natural language description. Example: A tool that shuffles a string."},
            "inputs": {"type": "string", "description": "Comma separated list of inputs and types. Example: query: str, api-token: str"},
            "outputs": {"type": "string", "description": "Comma separated list of outputs and types. Example: name: str, id: str"},
            "class_name": {"type": "string", "description": "Generated tool class name. This should uniquely identify the tool."}
    },
    "required": ["name", "description", "inputs", "outputs", "class_name"]
}

class GenerationTool(BaseTool):
    agent: ToolGenerationAgent = None
    tool_mgr: ToolManager = None

    def __init__(self, llm: ChatBot, tool_manager: ToolManager):
        super().__init__(name=name, description=description, parameters=parameters)
        self.agent = ToolGenerationAgent(llm)
        self.tool_mgr = tool_manager

    async def _generate_code(self, spec: str) -> str:
        return await self.agent.run(spec)

    async def execute(self, name: str, description: str, inputs: str, outputs: str, class_name: str = "GeneratedTaskTool") -> str:
        print(f"Attempting to generate {class_name}.")

        raw = await self._generate_code(f"name: \"{name}\", description: \"{description}\", inputs: \"{inputs}\", outputs: \"{outputs}\"")

        final_code = gen_code(raw, inputs, class_name, name)
        
        try:
            compile(final_code, "<string>", "exec")
        except SyntaxError as e:
            print(f"SyntaxError: {e.msg}")
            print(f"Line: {e.lineno}")
            print(f"Problem: {e.text}")
            return "Failed to generate code. Try again, or if this fails consistently, this may not be possible."


        parse_packages(final_code)

        out_dir = os.path.join(os.getcwd(), "generated-tools")
        os.makedirs(out_dir, exist_ok=True)
        out_path = tool_path(class_name, out_dir)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_code)

        load_tool(self.tool_mgr, out_path, class_name)

        return f"Successfully generated tool with name {name}"

# Retool

name2: str = "retool"
desc2: str ="Rebuilds a tool with further input. Use to fix broken tools."
params2: dict = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "The name of the function. Distinct from class_name."},
        "description": {"type": "string", "description": "Natural language description. Example: A tool that shuffles a string."},
        "inputs": {"type": "string", "description": "Comma separated list of inputs and types. Example: query: str, api-token: str"},
        "outputs": {"type": "string", "description": "Comma separated list of outputs and types. Example: name: str, id: str"},
        "class_name": {"type": "string", "description": "Generated tool class name."},
        "inference_args": {"type": "string", "description": "Additional information about what was problematic with the previous iteration of the tool."} 
    },       
    "required": ["name", "description", "inputs", "outputs", "class_name", "inference_args"]
}

class ReTool(BaseTool):
    agent: RetoolAgent = None
    tool_mgr: ToolManager = None

    def __init__(self, llm: ChatBot, tool_manager: ToolManager):
        super().__init__(name=name2, description=desc2, parameters=params2)
        self.agent = RetoolAgent(llm)
        self.tool_mgr = tool_manager

    async def _generate_code(self, spec: str) -> str:
        return await self.agent.run(spec)

    async def execute(self, name: str, description: str, inputs: str, outputs: str, class_name: str, inference_args: str) -> str:
        print(f"Attempting to rebuild {class_name}.")
        
        out_dir = os.path.join(os.getcwd(), "generated-tools")
        path = tool_path(class_name, out_dir)
        prev_code = ""
        with open(path, 'r') as file:
            prev_code = file.read()

        raw = await self._generate_code(f"name: \"{name}\", description: \"{description}\", inputs: \"{inputs}\", outputs: \"{outputs}\"\n"\
            f"Previous Iteration:\n"\
            f"{prev_code}\n"\
            f"Feedback:\n" \
            f"{inference_args}")
        final_code = gen_code(raw, inputs, class_name, name)
        
        try:
            compile(final_code, "<string>", "exec")
        except SyntaxError as e:
            print(f"SyntaxError: {e.msg}")
            print(f"Line: {e.lineno}")
            print(f"Problem: {e.text}")
            return "Failed to generate code. Try again, or if this fails consistently, this may not be possible."


        parse_packages(final_code)

        out_path = tool_path(class_name, out_dir)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_code)

        load_tool(self.tool_mgr, out_path, class_name)

        return f"Successfully rebuilt tool with name {name}"
