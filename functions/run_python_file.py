import os
import subprocess

from functions.get_files_info import is_permitted_directory


def run_python_file(working_directory, file_path, args=None):
    working_dir_abs: str = os.path.abspath(working_directory)
    py_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

    if not is_permitted_directory(working_dir_abs, py_file):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(py_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'

    file_name, file_extension = os.path.splitext(py_file)
    if file_extension != ".py":
        return f'Error: "{file_path}" is not a Python file'

    command = ["python", py_file]
    if args:
        command.extend(args)

    output = ""
    try:
        completed_process = subprocess.run(
            command,
            cwd=working_dir_abs,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
        )
    except Exception as e:
        return f"Error: executing Python file: {e}"

    if completed_process.returncode != 0:
        return f"Process exited with code {completed_process.returncode}"
    if not completed_process.stderr and not completed_process.stdout:
        return "No output produced"
    else:
        output += (
            f"STDOUT: {completed_process.stdout if completed_process.stdout else '\n'}"
        )
        output += (
            f"STDERR: {completed_process.stderr if completed_process.stderr else '\n'}"
        )

    return output
