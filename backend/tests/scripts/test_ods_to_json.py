import pytest

from scripts.ods_to_json import create_nested_dict


def test_create_nested_dict():
    source = {"a": "1", "b.c": "3", "d.0": "4", "d.1.a": "5"}
    dest = {"a": "1", "b": {"c": "3"}, "d": ["4", {"a": "5"}]}
    assert create_nested_dict(source) == dest


def test_create_nested_dict_fails():
    source = {"a": "1", "a.b": "2"}
    with pytest.raises(TypeError):
        create_nested_dict(source)
