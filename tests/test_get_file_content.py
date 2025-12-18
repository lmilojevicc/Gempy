import os

from functions.get_file_content import get_file_content


def test_get_valid_file_content(tmp_path):
    working_dir = str(tmp_path)

    file_name = "test.txt"
    file_path = tmp_path / file_name
    file_path.write_text("Hello world")

    content = get_file_content(working_dir, file_path)
    content = content.strip("\n").strip().lower()

    assert "hello world" in content


def test_get_valid_file_content_in_sub_dir(tmp_path):
    working_dir = str(tmp_path)
    dir = "pkg"
    os.mkdir(os.path.join(working_dir, dir))

    file_name = "test.txt"
    file_path = tmp_path / "pkg" / file_name
    file_path.write_text("Hello world")

    content = get_file_content(working_dir, file_path)
    content = content.strip("\n").strip().lower()

    assert "hello world" in content


def test_get_file_content_restricted_dir(tmp_path):
    working_dir = str(tmp_path)
    file_path = "/bin/cat"

    content = get_file_content(working_dir, file_path)
    content = content.strip("\n").strip().lower()

    assert content.startswith("error: ")
    assert content.endswith("outside the permitted working directory")


def test_get_file_content_non_existent_file(tmp_path):
    working_dir = str(tmp_path)
    file = "fake.txt"

    content = get_file_content(working_dir, file)
    content = content.strip("\n").strip().lower()

    assert content.startswith("error: ")
    assert "not found" in content
