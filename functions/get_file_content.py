import os

from google.genai import types

from config import MAX_CHARS
from functions.get_files_info import is_permitted_directory

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file contents for a relative path inside the permitted working directory. Returns up to MAX_CHARS characters; if the file is longer the output is truncated and a notice is appended.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=" Relative path to the target file (resolved against the working directory). Must be inside the permitted directory.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    working_dir_abs = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    if not is_permitted_directory(working_dir_abs, target_file_path):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    file_content = ""

    try:
        with open(target_file_path, "r") as f:
            file_content = f.read(MAX_CHARS)
            if f.read(1):
                file_content += (
                    f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
    except Exception:
        return f'Error: Cannot read "{file_path}"'

    return file_content
