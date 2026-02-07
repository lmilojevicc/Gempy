import os

from functions.run_python_file import run_python_file


def test_run_python_file_success(tmp_path):
    working_dir = str(tmp_path)
    file_name = "test_script.py"
    file_path = os.path.join(working_dir, file_name)

    with open(file_path, "w") as f:
        f.write("print('Hello from test script')")

    result = run_python_file(working_dir, file_name)
    assert "Hello from test script" in result


def test_run_python_file_with_args(tmp_path):
    working_dir = str(tmp_path)
    file_name = "test_args.py"
    file_path = os.path.join(working_dir, file_name)

    with open(file_path, "w") as f:
        f.write("import sys\nprint(f'Args: {sys.argv[1:]}')")

    # The run_python_file function expects args to be a list of strings
    result = run_python_file(working_dir, file_name, args=["arg1", "arg2"])
    assert "Args: ['arg1', 'arg2']" in result


def test_run_python_file_outside_working_dir(tmp_path):
    working_dir = str(tmp_path / "work")
    os.makedirs(working_dir)
    outside_dir = str(tmp_path / "outside")
    os.makedirs(outside_dir)

    file_name = "bad_script.py"
    file_path = os.path.join(outside_dir, file_name)

    with open(file_path, "w") as f:
        f.write("print('Should not run')")

    rel_path = os.path.join("..", "outside", file_name)

    result = run_python_file(working_dir, rel_path)
    assert "Error: Cannot execute" in result
    assert "outside the permitted working directory" in result


def test_run_non_existent_file(tmp_path):
    working_dir = str(tmp_path)
    result = run_python_file(working_dir, "ghost.py")
    assert "does not exist" in result or "not a regular file" in result


def test_run_non_python_file(tmp_path):
    working_dir = str(tmp_path)
    file_name = "test.txt"
    file_path = os.path.join(working_dir, file_name)

    with open(file_path, "w") as f:
        f.write("Not python code")

    result = run_python_file(working_dir, file_name)
    assert "is not a Python file" in result
