import os

from google.genai import types

from functions.get_files_info import is_permitted_directory

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write text content to a file inside the permitted working directory. "
    "Creates parent directories if necessary. Returns a success message with the number of characters written, "
    "or an error message if writing is not allowed or fails.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path to the target file"
                "Must be located inside the permitted working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write to the file. Existing files will be overwritten.",
            ),
        },
    ),
)


def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs: str = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

    if not is_permitted_directory(working_dir_abs, target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

    try:
        with open(target_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: Cannot write to "{file_path}": {e}'
