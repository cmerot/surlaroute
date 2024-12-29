import logging
import os
import sys
import typing
from typing import Any, TypeVar

import pytest
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)

from app.core.db.models import Base
from scripts.lib import (
    add_polymorphic_discriminator,
    get_input_file_path,
    get_submodel_class,
    populate_model_from_dict,
    set_logger,
)
from scripts.lib import logger as original_logger


@typing.no_type_check
def test_populate_model_from_dict() -> None:
    T = TypeVar("T", bound=DeclarativeBase)

    # Define a get_db_instance function for testing
    def get_db_instance(cls: type[T], data: dict[str, Any] | None = None) -> T:  # noqa: ARG001
        return cls()

    # Create a test class
    class Parent(Base):
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String)

    # Test with a nested relationship
    class Child(Base):
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String)
        parent_id: Mapped[int] = mapped_column(ForeignKey("parent.id"))
        parent: Mapped[Parent] = relationship(foreign_keys=[parent_id])

    # Create test data
    data: dict[str, Any] = {"name": "Child name", "parent": {"name": "Parent name"}}

    # Call populate_model_from_dict
    populated_instance = populate_model_from_dict(
        get_db_instance=get_db_instance,
        cls=Parent,
        data=data["parent"],
    )

    # Assert the instance was populated correctly
    assert populated_instance.name == data["parent"]["name"]

    # Call populate_model_from_dict
    populated_instance = populate_model_from_dict(
        get_db_instance=get_db_instance,
        cls=Child,
        data=data,
    )

    # # Assert the instance and its nested relationship were populated correctly
    assert populated_instance.name == data["name"]
    assert populated_instance.parent.name == data["parent"]["name"]

    populated_instance = populate_model_from_dict(
        get_db_instance=get_db_instance,
        cls=Child,
        data=data,
        instance=Child(name="To be updated"),
    )
    assert populated_instance.name == data["name"]


def test_add_polymorphic_discriminator_with_dict() -> None:
    data = {
        "actor#Person": {"name": "John"},
        "movie#Film": {"title": "Inception", "director": {"name": "Nolan"}},
    }
    expected_output = {
        "actor": {"name": "John", "type": "Person"},
        "movie": {"title": "Inception", "type": "Film", "director": {"name": "Nolan"}},
    }
    assert add_polymorphic_discriminator(data) == expected_output


def test_add_polymorphic_discriminator_with_list() -> None:
    data = [
        {"actor#Person": {"name": "John"}},
        {"movie#Film": {"title": "Inception", "director": {"name": "Nolan"}}},
    ]
    expected_output = [
        {"actor": {"name": "John", "type": "Person"}},
        {
            "movie": {
                "title": "Inception",
                "type": "Film",
                "director": {"name": "Nolan"},
            }
        },
    ]
    assert add_polymorphic_discriminator(data) == expected_output


def test_add_polymorphic_discriminator_with_nested_dict() -> None:
    data = {
        "library": {
            "books#Collection": {
                "title": "Science Fiction",
                "book#Book": {"title": "Dune"},
            }
        }
    }
    expected_output = {
        "library": {
            "books": {
                "title": "Science Fiction",
                "type": "Collection",
                "book": {"title": "Dune", "type": "Book"},
            }
        }
    }
    assert add_polymorphic_discriminator(data) == expected_output


@typing.no_type_check
def test_get_submodel_class() -> None:
    class NotPolymorph(Base):
        id: Mapped[int] = mapped_column(primary_key=True)

    class Polymorph(Base):
        id: Mapped[int] = mapped_column(primary_key=True)
        type: Mapped[str] = mapped_column(String)

        @declared_attr.directive
        def __mapper_args__(cls) -> dict[str, Any]:
            if cls.__name__ == "MyClass":
                return {
                    "polymorphic_on": cls.type,
                    "polymorphic_identity": cls.__name__,
                    "confirm_deleted_rows": False,
                }
            else:
                return {
                    "polymorphic_identity": cls.__name__,
                }

    class SubPolymorph(Polymorph):
        id: Mapped[int] = mapped_column(
            ForeignKey("polymorph.id"),
            primary_key=True,
        )

    # Test case: No polymorphic identity
    value = {}
    assert get_submodel_class(NotPolymorph, value) == NotPolymorph

    # Test case: With polymorphic identity
    value = {"type": "SubPolymorph"}
    assert get_submodel_class(Polymorph, value) == SubPolymorph


@typing.no_type_check
def test_get_input_file_path_successful_file(
    monkeypatch: pytest.MonkeyPatch, tmp_path: str
) -> None:
    """
    Test that get_input_file_path returns the absolute path of an existing file
    """
    # Create a temporary file
    test_file = tmp_path / "test_input.txt"
    test_file.write_text("Test content")

    # Modify sys.argv to include the file path
    monkeypatch.setattr(sys, "argv", ["script_name", str(test_file)])

    # Call the function
    result = get_input_file_path()

    # Assert the result is the absolute path of the test file
    assert result == str(test_file.resolve())


@typing.no_type_check
def test_get_input_file_path_no_arguments(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """
    Test that the function exits when no file path is provided
    """
    # Modify sys.argv to have only the script name
    monkeypatch.setattr(sys, "argv", ["script_name"])

    # Expect the function to exit
    with pytest.raises(SystemExit) as excinfo:
        get_input_file_path()

    # Check the exit code is 1
    assert excinfo.value.code == 1

    # Verify the usage message is printed
    captured = capsys.readouterr()
    assert f"Usage: {sys.argv[0]} <file_path>" in captured.out


@typing.no_type_check
def test_get_input_file_path_nonexistent_file(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture,
) -> None:
    """
    Test that the function exits when the provided file does not exist
    """
    # Create a path to a file that does not exist
    nonexistent_file = "/path/to/nonexistent/file.txt"

    # Modify sys.argv to include the nonexistent file path
    monkeypatch.setattr(sys, "argv", ["script_name", nonexistent_file])

    # Expect the function to exit
    with pytest.raises(SystemExit) as excinfo:
        get_input_file_path()

    # Check the exit code is 1
    assert excinfo.value.code == 1

    # Verify the error message is printed
    captured = capsys.readouterr()
    assert (
        f"Error: The file '{os.path.abspath(nonexistent_file)}' was not found."
        in captured.out
    )


def test_set_logger_changes_global_logger() -> None:
    """
    Test that set_logger successfully changes the global logger
    """
    # Create a new logger
    new_logger = logging.getLogger("test_logger")
    new_logger.setLevel(logging.DEBUG)

    # Call set_logger with the new logger
    set_logger(new_logger)

    try:
        # Import the module again to get the updated logger
        from scripts.lib import logger

        # Check that the global logger has been updated
        assert logger == new_logger, "Global logger was not updated"

        # Verify that the new logger is different from the original
        assert logger is not original_logger, "Logger reference should be different"
    finally:
        # Reset the logger back to the original to avoid side effects
        set_logger(original_logger)
