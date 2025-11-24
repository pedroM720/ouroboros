import os
import importlib.util
import inspect
from typing import List
from spoon_ai.tools.tool_manager import ToolManager
from spoon_ai.tools.base import BaseTool

def load_tool(tool_manager: ToolManager, tool_path : str, fname: str) -> None:
    print(f"Loading {tool_path}")

    mod_name = f"generated_tools.{os.path.splitext(fname)[0]}"
    
    spec = importlib.util.spec_from_file_location(mod_name, tool_path)
    if not spec or not spec.loader:
        print("failed to load spec")
        return

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(e)
        return
    for _, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, BaseTool) and obj is not BaseTool:
            try:
                tool = obj()
                name = getattr(tool, "name", None)
                
                print(f"{name} loaded!")
                tool_manager.add_tool(tool)
            except Exception as e:
                print(e)
                continue
