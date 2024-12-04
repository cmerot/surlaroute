#!/usr/bin/env python
# mypy: ignore-errors

import json
import os

import pyexcel as pe


def create_nested_dict(flat_dict: dict) -> dict:
    def insert(d: dict, keys: list[str], value: str):
        key = keys[0]
        if key.isdigit():
            key = int(key)

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

    nested_dict = {}
    for key, value in flat_dict.items():
        keys = key.split(".")
        insert(nested_dict, keys, value)

    return nested_dict


def get_path(relative_path: str) -> str:
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Build the full path
    full_path = os.path.join(script_dir, relative_path)
    return full_path


input = get_path("../fixtures/private/data.ods")
output = get_path("../fixtures/private/data.json")

if __name__ == "__main__":
    data = {}

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
