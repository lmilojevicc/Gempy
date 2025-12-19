from google.genai import types

from functions.get_files_info import schema_get_files_info

MAX_CHARS = 10000
MODEL_NAME = "gemini-2.5-flash"
SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
AVAILABLE_FUNCS = types.Tool(function_declarations=[schema_get_files_info])
