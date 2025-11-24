import os
import importlib.util
import inspect
from typing import List
from spoon_ai.tools.tool_manager import ToolManager
from spoon_ai.tools.base import BaseTool

def load_tool(tool_manager: ToolManager, tool_path : str, fname: str) -> None:
    """
    Helper function to load a single tool file.
    """
    # print(f"Loading {tool_path}") # Optional: verify path

    mod_name = f"generated_tools.{os.path.splitext(fname)[0]}"
    
    try:
        spec = importlib.util.spec_from_file_location(mod_name, tool_path)
        if not spec or not spec.loader:
            # print("failed to load spec")
            return

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"Error loading module {fname}: {e}")
        return

    existing_tools = getattr(tool_manager, "tool_map", {})

    for _, obj in inspect.getmembers(module, inspect.isclass):
        if issubclass(obj, BaseTool) and obj is not BaseTool:
            try:
                tool = obj()
                name = getattr(tool, "name", None)
                
                # Avoid re-adding if it already exists
                if name and name in existing_tools:
                    continue
                
                print(f"⚡ Reflex Loaded: {name}")
                tool_manager.add_tool(tool)
            except Exception as e:
                print(f"Error instantiating tool {obj}: {e}")
                continue

def load_generated_tools(tool_manager: ToolManager, dir_path: str = "./generated-tools") -> None:
    """
    Main entry point used by AdaptiveAgent.
    Scans the directory and calls load_tool for each .py file.
    """
    if not os.path.isdir(dir_path):
        return

    for fname in os.listdir(dir_path):
        if not fname.endswith(".py"):
            continue
            
        tool_path = os.path.join(dir_path, fname)
        load_tool(tool_manager, tool_path, fname)