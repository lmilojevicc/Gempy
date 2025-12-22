# Gempy

Gempy is an autonomous command-line AI coding agent built from scratch using Python and Google Gemini API. Created to demystify AI agent architecture, it demonstrates how function calling provides codebase context and how feedback loops enable autonomous operation.

## Core Functionality

The agent utilizes an agentic loop powered by function calling to perform autonomous tasks. Key technical features include:

- **Function Calling:** Implementing tools that allow the LLM to choose and execute specific Python functions.
- **Feedback Loops:** Creating a cycle where the agent executes code, receives output or error messages, and adjusts its next actions to resolve bugs.
- **Code Manipulation:** The ability to read existing project files, write new content, and run scripts to verify fixes.

## Built-in Tools

The agent is equipped with the following tools to interact with the project environment:

| Tool               | Functionality                                                   |
| :----------------- | :-------------------------------------------------------------- |
| `get_files_info`   | Lists files and directories in the project.                     |
| `get_file_content` | Reads the content of a specific file for analysis.              |
| `write_file`       | Creates or updates files with new code.                         |
| `run_python_file`  | Executes Python files and returns the standard output or error. |
