# Coding Agent

An AI-powered coding agent built from scratch using Google's Gemini 2.5 Flash model. It reads, writes, and executes files within a sandboxed working directory — all driven from the terminal via natural language prompts.

The `calculator/` submodule serves as the test repo the agent operates on.

## How It Works

```
User prompt (terminal) → Gemini 2.5 Flash → Function calls → Tool execution → Loop until done
```

1. The user provides a natural language prompt via the CLI
2. The prompt is sent to Gemini along with a system prompt and tool declarations
3. Gemini responds with function calls (read a file, list a directory, write a file, run a script)
4. The agent executes those calls and feeds results back to Gemini
5. This agentic loop continues (up to 20 iterations) until Gemini produces a final text response

```bash
uv run main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20"
```

## Project Structure

```
coding-agent/
├── main.py                  # Entry point — agentic loop with Gemini
├── prompts.py               # System prompt with guardrails
├── call_function.py         # Function dispatcher, injects working_directory
├── config.py                # Constants (MAX_CHARS for file reads)
├── functions/               # Tool implementations exposed to the LLM
│   ├── get_files_info.py    # List directory contents
│   ├── get_file_content.py  # Read file contents (truncated at 10k chars)
│   ├── write_file.py        # Write/overwrite files
│   └── run_python_file.py   # Execute Python files with optional args
├── test_get_files_info.py   # Tests for directory listing
├── test_get_file_content.py # Tests for file reading
├── test_write_file.py       # Tests for file writing
├── test_run_python_file.py  # Tests for Python execution
└── calculator/              # Target repo the agent operates on
    ├── main.py
    ├── tests.py
    └── pkg/
        ├── calculator.py
        └── render.py
```

## Key Lessons: Guardrails for LLM Tool Use

### 1. Sandboxing the working directory

Every tool function receives a `working_directory` parameter injected server-side in `call_function.py` — the LLM never controls it. Each function validates paths with `os.path.commonpath` to ensure the LLM cannot escape the sandbox:

```python
# The LLM cannot request paths outside the working directory
if os.path.commonpath([abs_working_dir, abs_file_path]) != abs_working_dir:
    return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
```

This blocks attempts like `../../etc/passwd` or `/bin/cat`.

### 2. Returning errors instead of raising exceptions

Since the LLM is the caller, functions return error strings rather than raising exceptions. This gives the model a chance to self-correct instead of crashing the agent loop.

### 3. System prompt guardrails for intent understanding

The system prompt explicitly tells the LLM to interpret natural language — not blindly pass user input as program arguments. Without this, a prompt like `"Fix the bug: 3 + 7 * 2 shouldn't be 20"` would get forwarded as raw args to `main.py`, producing `Error: invalid token: Fix`. The prompt instructs the agent to:

- Understand user intent before acting
- Read code before writing code
- Extract only valid program arguments from natural language
- Follow a diagnose-fix-verify workflow for bug reports

### 4. Testing tool functions before giving them to the LLM

Each function in `functions/` has a corresponding test file that validates behavior *before* the LLM ever uses it. Tests cover:

- Happy path (valid directories, files, expressions)
- Path traversal attempts (`../`, `/bin`, `/tmp`)
- Non-existent files and directories
- Non-Python file execution attempts
- File truncation for large files

This ensures the guardrails actually work — a bug in `get_file_content` that lets the LLM read `/etc/passwd` would be caught here, not in production.

## Setup

```bash
# Install dependencies
uv sync

# Set your Gemini API key
echo "GEMINI_API_KEY=your_key_here" > .env

# Run the agent
uv run main.py "your prompt here"

# Verbose mode (shows token usage and function call details)
uv run main.py "your prompt here" --verbose
```

## Learning Goals

- Get an introduction to multi-directory Python projects
- Understand how AI coding tools actually work under the hood
- Practice Python and functional programming skills
- Build an agent from scratch using a pre-trained LLM
