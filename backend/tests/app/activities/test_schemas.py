import pytest
from pydantic import ValidationError

from app.activities.schemas import TreePublic


def test_tree_public_schema_valid() -> None:
    valid_data = {"name": "Test Activity", "path": "test.path"}

    tree_public = TreePublic.model_validate(valid_data)

    assert tree_public.name == valid_data["name"]
    assert tree_public.path == valid_data["path"]


def test_tree_public_schema_missing_fields() -> None:
    invalid_data = {
        "path": "test.path"  # Missing 'name'
    }

    with pytest.raises(ValidationError):
        TreePublic.model_validate(invalid_data)
