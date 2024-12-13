#!/usr/bin/env python

import json
from typing import Any

import pyexcel as pe  # type: ignore[import-untyped]

from scripts.lib import get_input_file_path


def create_nested_dict(flat_dict: dict[str, Any]) -> dict[str, Any]:
    """
    Transform a flat dict to a nested dict. Example:
    {
        "a": "1",
        "b.c": "3",
        "d.0": "4",
        "d.1.name": "5"
    }

    becomes:

    {
        "a": "1",
        "b": {
            "c": "3"
        },
        "d": [
            "4",
            {"name": "5"}
        ]
    }
    """

    def insert(d: dict[str, Any], keys: list[str], value: str) -> None:
        key = keys[0]
        if key.isdigit():
            key = int(key)  # type: ignore[assignment]

        if len(keys) == 1:
            if isinstance(key, int):
                while len(d) <= key:
                    d.append(None)
                d[key] = value
            else:
                d[key] = value
        else:
            if isinstance(key, int):
                while len(d) <= key:
                    d.append({})
                if d[key] is None:
                    d[key] = {}
                if value != "":
                    insert(d[key], keys[1:], value)
            else:
                if key not in d:
                    d[key] = {} if not keys[1].isdigit() else []
                if value != "":
                    insert(d[key], keys[1:], value)

    nested_dict: dict[str, Any] = {}
    for key, value in flat_dict.items():
        keys = key.split(".")
        insert(nested_dict, keys, value)

    return nested_dict


if __name__ == "__main__":
    input = get_input_file_path()
    output = input.rsplit(".", 1)[0] + ".json"

    data: dict[str, Any] = {}

    workbook = pe.get_book(file_name=input)

    for sheet_name in workbook.sheet_names():
        print(sheet_name)
        sheet_records = pe.iget_records(
            file_name=input, sheet_name=sheet_name, skip_empty_rows=True, data_only=True
        )

        data[sheet_name] = []
        for r in list(sheet_records):
            r_dict = {}
            for k, v in r.items():
                r_dict[k] = v
            data[sheet_name].append(create_nested_dict(r_dict))

    with open(output, "w") as json_file:
        json.dump(data, json_file, indent=4)
