import sys
import importlib
import importlib.util
from pathlib import Path
from tool_constructor import ToolConstructor, ToolGenerationTool


class AdaptiveAgent:
    def __init__(self):
        self.tools = {}
        self.tool_gen = ToolGenerationTool(ToolConstructor())

    def use_tool(self, name, *args, **kwargs):
        if name not in self.tools:
            code = self.generate_tool_code(name, *args, **kwargs)
            func = self.tool_gen.generate(name, code)
            self.tools[name] = func
        return self.tools[name](*args, **kwargs)

    def generate_tool_code(self, name, *args, **kwargs):
        if name == "word_count":
            return (
                "def word_count(text):\n"
                "    return len(text.split())\n"
            )
        if name == "uppercase":
            return (
                "def uppercase(s):\n"
                "    return s.upper()\n"
            )
        return (
            f"def {name}(*args, **kwargs):\n"
            "    return {'args': args, 'kwargs': kwargs}\n"
        )


def main():
    agent = AdaptiveAgent()
    text = "SpoonOS enables dynamic tools."
    count = agent.use_tool("word_count", text)
    print(count)
    upper = agent.use_tool("uppercase", "adaptability")
    print(upper)
    echo = agent.use_tool("unknown_tool", 1, 2, x=3)
    print(echo)


if __name__ == "__main__":
    main()