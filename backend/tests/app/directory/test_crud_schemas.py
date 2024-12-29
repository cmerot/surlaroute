import json
from typing import Any

import geoalchemy2
import geojson_pydantic
import pytest
import shapely.geometry

from app.directory.crud_schemas import (
    serialize_geom_point,
    validate_geom_point,
    validate_json,
)


def test_validate_json_with_string() -> None:
    # Test case: Input is a string
    input_value = "This is a test string"
    expected_output = "This is a test string"
    assert validate_json(input_value) == expected_output


def test_validate_json_with_dict() -> None:
    # Test case: Input is a dictionary
    input_value = {"key": "value"}
    expected_output = json.dumps(input_value)
    assert validate_json(input_value) == expected_output


def test_validate_json_with_empty_dict() -> None:
    # Test case: Input is an empty dictionary
    input_value: dict[str, Any] = {}
    expected_output = json.dumps(input_value)
    assert validate_json(input_value) == expected_output


def test_validate_json_with_nested_dict() -> None:
    # Test case: Input is a nested dictionary
    input_value = {"key1": "value1", "key2": {"nested_key": "nested_value"}}
    expected_output = json.dumps(input_value)
    assert validate_json(input_value) == expected_output


def test_validate_geom_point_with_wkbelement() -> None:
    point = shapely.geometry.Point(1.1, 2.2)
    wkbelement = geoalchemy2.shape.from_shape(point)
    assert validate_geom_point(wkbelement) == wkbelement


def test_validate_geom_point_with_string() -> None:
    input_value = "1.1, 2.2"
    point = shapely.geometry.Point(1.1, 2.2)
    wkbelement = geoalchemy2.shape.from_shape(point)
    assert validate_geom_point(input_value) == wkbelement


def test_validate_geom_point_with_invalid_string() -> None:
    input_value = "invalid_string"
    with pytest.raises(
        ValueError,
        match="geom_point must be a string in the format 'lat, lon' eg: '1.1, 2.2'",
    ):
        validate_geom_point(input_value)


def test_validate_geom_point_with_basegeometry() -> None:
    point = shapely.geometry.Point(1.1, 2.2)
    wkbelement = geoalchemy2.shape.from_shape(point)
    assert validate_geom_point(point) == wkbelement


def test_serialize_geom_point_with_geojson_pydantic_point() -> None:
    coordinates = geojson_pydantic.types.Position2D(latitude=1.1, longitude=2.2)
    point = geojson_pydantic.Point(type="Point", coordinates=coordinates)
    assert serialize_geom_point(point) == point


def test_serialize_geom_point_with_wkbelement() -> None:
    point = shapely.geometry.Point(1.1, 2.2)
    wkbelement = geoalchemy2.shape.from_shape(point)
    result = serialize_geom_point(wkbelement)
    assert isinstance(result, geojson_pydantic.Point)
    assert result.coordinates.longitude == 2.2
    assert result.coordinates.latitude == 1.1
