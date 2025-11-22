## Overview
- Add a dedicated agent (`ToolConstructor`) that builds missing tools on demand.
- Route tool creation through a tool interface (`ToolGenerationTool`), so `AdaptiveAgent` no longer writes files directly.
- Preserve dynamic import and hot-reload of `my_new_tool.py` while improving separation of concerns.

## New Components
- `tool_constructor.py`
  - `ToolConstructor`: builds a tool by writing source to `my_new_tool.py`, loads/refreshes the module, and returns a callable.
  - `ToolGenerationTool`: thin wrapper that `AdaptiveAgent` queries; delegates to `ToolConstructor` and returns the newly built function.

## Refactors
- `agent.py`
  - Inject `ToolGenerationTool` into `AdaptiveAgent` (composition over direct file I/O).
  - Replace inline write/import logic in `use_tool` (`agent.py:16-30`) with a call to `ToolGenerationTool.generate(name, code)`.
  - Keep `generate_tool_code` (`agent.py:33-47`) to produce the initial source for known tools; pass this code to `ToolGenerationTool`.

## Data Flow
- `AdaptiveAgent.use_tool(name, *args, **kwargs)` → checks registry.
- If missing: `code = generate_tool_code(...)` → `ToolGenerationTool.generate(name, code)` → `ToolConstructor.build_tool(name, code)` → writes/loads `my_new_tool.py` → returns `callable` → registered in `AdaptiveAgent.tools` → executed.

## Implementation Steps
1. Create `tool_constructor.py` with:
   - `ToolConstructor.__init__(module_name="my_new_tool", module_path=Path("my_new_tool.py"))`.
   - `build_tool(name, code)`: write `code`, import/reload module, return `getattr(module, name)`; raise informative errors if missing.
   - `ToolGenerationTool.__init__(constructor: ToolConstructor)` and `generate(name, code)` returning the callable.
2. Update `agent.py`:
   - Add imports from `tool_constructor.py`.
   - Add `self.tool_gen = ToolGenerationTool(ToolConstructor())` in `AdaptiveAgent.__init__` (`agent.py:7-12`).
   - In `use_tool` (`agent.py:14-31`): on miss, call `self.tool_gen.generate(name, code)` instead of writing files and reloading.
   - Keep the public behavior and demo in `main()` (`agent.py:50-62`).
3. Error handling and robustness:
   - Validate `code` defines the requested `name`; raise with actionable message if not.
   - Handle loader absence and attribute lookup failures with clear exceptions.
   - Ensure idempotent reload behavior when module exists.
4. Minimal, comment-free code to match current style; no external dependencies.

## Validation
- Run `python agent.py` and verify outputs remain:
  - `word_count("SpoonOS enables dynamic tools.")` → `4`.
  - `uppercase("adaptability")` → `ADAPTABILITY`.
  - `unknown_tool(1, 2, x=3)` → echoes args/kwargs.
- Confirm `my_new_tool.py` regenerates and hot-reloads without manual intervention.

## Risks & Mitigations
- Attribute not found after write: assert function exists before returning; raise descriptive error.
- Reload inconsistencies: always use `importlib.reload` when module present, otherwise `spec_from_file_location` with `exec_module`.
- Path issues on Windows: use `Path` consistently.

## Deliverables
- New `tool_constructor.py` with `ToolConstructor` and `ToolGenerationTool`.
- Refactored `agent.py` using the tool chain and retaining current demo behavior.
- Verified run with expected outputs; no new dependencies or comments.