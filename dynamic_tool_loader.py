import os
import importlib.util
import inspect
from typing import List
from spoon_ai.tools.tool_manager import ToolManager
from spoon_ai.tools.base import BaseTool

def load_generated_tools(tool_manager: ToolManager, dir_path: str = "./generated-tools") -> List[BaseTool]:
    loaded: List[BaseTool] = []
    
    if not os.path.isdir(dir_path):
        return loaded
    
    existing = set(getattr(tool_manager, "tool_map", {}).keys())

    for fname in os.listdir(dir_path):
        if not fname.endswith(".py"):
            continue
        print(f"{fname} detected")
        path = os.path.join(dir_path, fname)
        mod_name = f"generated_tools.{os.path.splitext(fname)[0]}"
        
        spec = importlib.util.spec_from_file_location(mod_name, path)
        if not spec or not spec.loader:
            continue

        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except Exception as e:
            print(e)
            continue
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, BaseTool) and obj is not BaseTool:
                try:
                    tool = obj()
                    name = getattr(tool, "name", None)
                    if name and name in existing:
                        continue
                    
                    print(f"{name} loaded!")
                    tool_manager.add_tool(tool)
                    loaded.append(tool)

                    if name:
                        existing.add(name)
                except Exception as e:
                    print(e)
                    continue
    return loaded