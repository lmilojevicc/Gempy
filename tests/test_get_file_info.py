import os

from functions.get_files_info import get_files_info


def test_valid_dir_list(tmp_path):
    working_dir = str(tmp_path)
    dir = "."
    file_path = tmp_path / "test.txt"
    file_path.write_text("Hello")

    output = get_files_info(working_dir, dir)
    output = output.lower().strip("\n")

    assert "result for current directory:" in output

    assert "file_size=" in output
    assert "is_dir=" in output


def test_valid_subdir_list(tmp_path):
    working_dir = str(tmp_path)
    dir = "pkg"
    os.mkdir(os.path.join(working_dir, dir))

    file_name = "test.txt"
    file_path = tmp_path / "pkg" / file_name
    file_path.write_text("Hello")

    output = get_files_info(working_dir, dir)
    output = output.lower().strip("\n")

    assert "result for current directory:" in output

    list_format = f"- {file_name}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}".lower()
    assert list_format in output


def test_restricted_dir(tmp_path):
    working_dir = str(tmp_path)
    dir = "/bin"

    output = get_files_info(working_dir, dir)
    output = output.lower().strip("\n")

    assert "error" in output
    assert output.endswith("outside the permitted working directory")


def test_back_dir(tmp_path):
    working_dir = str(tmp_path)
    dir = "../"

    output = get_files_info(working_dir, dir)
    output = output.lower().strip("\n")

    assert "error" in output
    assert output.endswith("outside the permitted working directory")


def test_non_dir_list(tmp_path):
    working_dir = str(tmp_path)
    dir = "/bin"

    output = get_files_info(working_dir, dir)
    output = output.lower().strip("\n")

    assert "error" in output
    assert output.endswith("outside the permitted working directory")
