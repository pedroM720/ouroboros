import re
from typing import List, Tuple
from spoon_ai.tools.base import BaseTool
from spoon_ai.chat import ChatBot
import os

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
name: str = "generation_tool"
description: str = "Generate a BaseTool class file from agent output, preserving imports and run()"
parameters: dict = {
        "type": "object",
        "properties": {
            "spec": {"type": "string", "description": "Task generation spec or raw code"},
            "class_name": {"type": "string", "description": "Generated tool class name"}
    },
    "required": ["spec", "input"]
}
class GenerationTool(BaseTool):
    agent: ToolGenerationAgent = None

    def __init__(self, llm: ChatBot):
        super().__init__(name=name, description=description, parameters=parameters)
        self.agent = ToolGenerationAgent(llm)

    async def _generate_code(self, spec: str) -> str:
        return await self.agent.run(spec)

    async def execute(self, spec: str, class_name: str = "GeneratedTaskTool") -> str:
        raw = await self._generate_code(spec)
        latest = _extract_latest_step_code(raw)
        cleaned = _strip_code_fences(latest)
        imports, body = _extract_imports_and_body(cleaned)
        header = ["from spoon_ai.tools.base import BaseTool"] + imports
        assembled_parts = []
        assembled_parts.append("\n".join(header).strip())
        if body:
            assembled_parts.append("\n" + body + "\n")
        tool_class = (
            f"class {class_name}(BaseTool):\n"
            f"    name: str = \"{class_name.replace('Tool', '').lower()}\"\n"
            f"    description: str = \"Generated task tool\"\n"
            f"    parameters: dict = {{\n"
            f"        \"type\": \"object\",\n"
            f"        \"properties\": {{\n"
            f"            \"input\": {{\"type\": \"string\", \"description\": \"Input for run()\"}}\n"
            f"        }},\n"
            f"        \"required\": [\"input\"]\n"
            f"    }}\n"
            f"    async def execute(self, input: str) -> str:\n"
            f"        return await run(input)\n"
        )
        assembled_parts.append(tool_class)
        final_code = "\n".join(assembled_parts)
        
        try:
            compile(final_code, "<string>", "exec")
        except SyntaxError as e:
            return "Failed to generate code. Task may not be feasible for current generation models."

        out_dir = os.path.join(os.getcwd(), "generated-tools")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{class_name}.py")
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(final_code)

        return "Successfully generated tool."
        