import os

from functions.write_file import write_file


def test_write_to_valid_file(tmp_path):
    working_dir = str(tmp_path)
    file = "lorem.txt"
    content = "wait, this isn't lorem ipsum"

    result = write_file(working_dir, file, content)

    assert result.startswith("Successfully wrote to")

    file_path = os.path.join(working_dir, file)
    assert os.path.exists(file_path)

    with open(file_path, "r") as f:
        assert f.read() == content


def test_write_to_restricted_dir(tmp_path):
    working_dir = str(tmp_path)
    file = "/bin/bash"
    content = "won't work"

    result = write_file(working_dir, file, content).lower()

    print(result)
    assert result.startswith("error:")
    assert result.endswith("is outside the permitted working directory")


def test_write_to_dir(tmp_path):
    working_dir = str(tmp_path)
    dir = "test_dir"
    os.mkdir(os.path.join(working_dir, dir))
    content = "won't work"

    result = write_file(working_dir, dir, content).lower()

    assert result.startswith("error:")
    assert result.endswith("it is a directory")


def test_write_to_file_in_non_existen_directories(tmp_path):
    working_dir = str(tmp_path)
    dirs = "more/dirs/"
    file = "lorem.txt"
    target_file = dirs + file
    content = "wait, this isn't lorem ipsum"

    result = write_file(working_dir, target_file, content)

    assert result.startswith("Successfully wrote to")
    assert os.path.exists(os.path.normpath(working_dir + "/" + dirs))

    file_path = os.path.join(working_dir, target_file)
    assert os.path.exists(file_path)

    with open(file_path, "r") as f:
        assert f.read() == content
