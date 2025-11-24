🛑 SECURITY WARNING: DO NOT DEPLOY PUBLICLY 🛑

CRITICAL: This software is a Proof of Concept (PoC) intended strictly for local, sandboxed research.
NEVER DEPLOY THIS APPLICATION TO THE PUBLIC INTERNET.
This framework fundamentally relies on Arbitrary Code Execution (ACE). It autonomously generates, installs, and executes Python code on the host machine. Exposing this to the web is equivalent to giving root access to your server to any anonymous user.


Ouroboros: Adaptive Tool-Generation Framework
Ouroboros is a Python-based agentic framework that implements Just-In-Time (JIT) capability synthesis. Unlike standard tool-use agents that select from a fixed definition list, Ouroboros detects capability gaps at runtime and generates, validates, and persists executable Python code to resolve them.
The system is built on a Gemini 2.5 Flash backbone and utilizes a custom hot-loading mechanism to inject generated logic into the active runtime without restarting the process.

System Architecture
The core architecture consists of four distinct modules operating in a synchronous event loop.

1. The Runtime Agent (AdaptiveAgent)
Inheritance: Extends spoon_ai.agents.ToolCallAgent.

Behavior: Operates on a max_steps loop (default: 10). On every step, it performs a check against the ToolManager to see if new tools have been loaded from the filesystem.
Prompt Engineering: The system prompt is engineered to prioritize generalized tool creation over one-off solutions. It is explicitly instructed to handle implementation details internally and only request user input for missing authentication keys.

2. JIT Compiler & Sanitizer (GenerationTool)
This component is responsible for converting natural language specifications into executable Python classes.
Code Generation: Utilizes a specialized ToolGenerationAgent to draft Python code.
AST Validation: Before persistence, the code is passed through Python's built-in compile() function to catch SyntaxError exceptions early.

3. Dynamic Linker (dynamic_tool_loader.py)
This module acts as a hot-loader for the persistent tool cache.
Path Scanning: Monitors ./generated-tools/*.py.
Class Inspection: Uses importlib.util to load modules from file specs and inspect.getmembers to identify classes inheriting from BaseTool.
De-duplication: Maintains a set of loaded tool names to prevent registry collisions during the AdaptiveAgent.initialize() phase.

4. Session State Manager (server.py)

A FastAPI implementation that isolates agent memory.

State: Uses an in-memory dictionary agent_sessions: Dict[str, AdaptiveAgent] to map session_id to agent instances.
Reflex Detection: Calculates tool registry delta (len(tools_after) - len(tools_before)) per request to flag responses that triggered a JIT compilation event ("Reflex").

Installation & Setup

Requirements:

Python 3.10+
Environment with write access to the local filesystem (for ./generated-tools).
Internet access for pip installation of generated dependencies.

Config:
The system relies on the spoon-ai internal package. Ensure GEMINI_API_KEY is set in your environment variables.


Running the Server
The application exposes a REST API via FastAPI.
python server.py

💀 Critical Security Hazards

This framework is essentially aimed at your own machine. Do not run this on a machine containing sensitive personal data or one that is connected to critical networks.

1. Unrestricted Package Installation (pip install):
The system parses import statements from generated code and automatically runs pip install via subprocess.
Risk: The LLM could hallucinate (or be tricked into) installing a typo-squatted malicious package (e.g., requests instead of requests).
Consequence: Malicious code executes immediately upon installation, potentially establishing a reverse shell or installing ransomware.

2. Arbitrary Code Execution:
The GenerationTool executes whatever Python code the LLM writes.
Risk: An adversarial prompt could instruct the agent to write code that deletes system files (rm -rf /), modifies permissions, or creates infinite loops ("fork bombs").
Consequence: Total system instability, data loss, or hardware getting fried

3. Data Exfiltration:
Risk: If you provide the agent with sensitive keys (e.g., AWS, Stripe, OpenAI) to use in a tool, a generated script could theoretically be tricked to send those keys to a third-party server
