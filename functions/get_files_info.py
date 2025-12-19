import os

from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["directory"],
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def is_permitted_directory(working_dir_abs, directory):
    common_path = os.path.commonpath([working_dir_abs, directory])
    return common_path == working_dir_abs


def get_files_info(working_directory, directory="."):
    working_dir_abs: str = os.path.abspath(working_directory)
    target_dir: str = os.path.normpath(os.path.join(working_dir_abs, directory))

    if not is_permitted_directory(working_dir_abs, target_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{target_dir}" is not a directory'

    output = "Result for current directory:\n"
    for file in os.listdir(target_dir):
        path_to_file = os.path.join(target_dir, file)
        output += f"- {file}: file_size={os.path.getsize(path_to_file)} bytes, is_dir={os.path.isdir(path_to_file)}\n"

    return output
