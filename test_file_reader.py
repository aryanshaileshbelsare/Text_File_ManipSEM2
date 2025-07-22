
import sys, os
sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir, "src")
    )
)

  
import os
import pytest
from project_venv import CustomFile, MultiFile, ANSI_COLORS

import os
import pytest
from project_venv import CustomFile, MultiFile, ANSI_COLORS

@pytest.fixture
def tmp_txt_files(tmp_path):
    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("foo\nbar\n")
    b.write_text("baz\nqux\n")
    return str(a), str(b)

def test_read_lines_and_str(tmp_txt_files):
    a_path, _ = tmp_txt_files
    cf = CustomFile(a_path)
    assert list(cf.read_lines()) == ["foo", "bar"]
    assert a_path in str(cf)

def test_property_and_setter(tmp_txt_files):
    a_path, b_path = tmp_txt_files
    cf = CustomFile(a_path)
    assert cf.file == a_path
    cf.file = b_path
    assert cf.file == b_path

def test_has_txt_ext_and_create_all(tmp_txt_files):
    a_path, b_path = tmp_txt_files
    assert CustomFile.has_txt_ext(a_path)
    assert not CustomFile.has_txt_ext("nope.py")
    all_objs = CustomFile.create_all([a_path, b_path])
    assert [o.file for o in all_objs] == [a_path, b_path]

def test_add_operator_custom(tmp_txt_files):
    a_path, b_path = tmp_txt_files
    cf1, cf2 = CustomFile(a_path), CustomFile(b_path)
    merged = cf1 + cf2
    assert isinstance(merged, CustomFile)
    assert os.path.exists(merged.file)
    assert list(merged.read_lines()) == ["foo", "bar", "baz", "qux"]

def test_show_info_decorator(capsys, tmp_txt_files):
    a_path, _ = tmp_txt_files
    cf = CustomFile(a_path)
    cf.show_info()
    out = capsys.readouterr().out
    assert out.startswith(ANSI_COLORS["red"])
    assert a_path in out
    assert out.rstrip().endswith(ANSI_COLORS["reset"])

def test_multifile_concat(tmp_txt_files):
    a_path, b_path = tmp_txt_files
    cf1, cf2 = CustomFile(a_path), CustomFile(b_path)
    mf = MultiFile.concat(cf1, cf2, output_path="all.txt")
    assert isinstance(mf, MultiFile)
    assert mf.file == "all.txt"
    assert list(mf.read_lines()) == ["foo", "bar", "baz", "qux"]

def test_multifile_add(tmp_txt_files):
    a_path, b_path = tmp_txt_files
    cf1, cf2 = CustomFile(a_path), CustomFile(b_path)
    mf = MultiFile.concat(cf1, cf2, output_path="all2.txt")
    result = mf + cf2
    assert isinstance(result, MultiFile)
    assert result.file == "merged.txt"
    assert list(result.read_lines()) == ["foo", "bar", "baz", "qux", "baz", "qux"]

