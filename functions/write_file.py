import os

from functions.get_files_info import is_permitted_directory


def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs: str = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))

    if not is_permitted_directory(working_dir_abs, target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if os.path.isdir(target_file_path):
        return f'Error: Cannot write to "{file_path}" as it is a directory'

    dir_path = target_file_path.rindex("/")
    os.makedirs(target_file_path[:dir_path], exist_ok=True)

    try:
        with open(target_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except:
        return f'Error: Cannot write to "{file_path}"'
