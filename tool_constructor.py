import sys
import importlib
import importlib.util
from pathlib import Path


class ToolConstructor:
    def __init__(self, tools_dir=Path("generated_tools")):
        self.tools_dir = Path(tools_dir)
        self.tools_dir.mkdir(parents=True, exist_ok=True)

    def build_tool(self, name, code):
        module_name = f"generated_tools_{name}"
        module_path = self.tools_dir / f"{name}.py"
        module_path.write_text(code, encoding="utf-8")
        if module_name in sys.modules:
            module = importlib.reload(sys.modules[module_name])
        else:
            spec = importlib.util.spec_from_file_location(module_name, str(module_path))
            module = importlib.util.module_from_spec(spec)
            loader = spec.loader
            if loader is None:
                raise RuntimeError("loader unavailable")
            loader.exec_module(module)
            sys.modules[module_name] = module
        func = getattr(module, name, None)
        if func is None:
            raise AttributeError(name)
        return func


class ToolGenerationTool:
    def __init__(self, constructor):
        self.constructor = constructor

    def generate(self, name, code):
        return self.constructor.build_tool(name, code)