import re
from geometry_utils import Vector


def parse_file(file_name):
    with open(file_name) as fp:
        data = fp.read()
    return parse_data(data)


def parse_data(data: str):
    all_scanners_data = re.split(r"--- scanner \d+ ---", data, flags=re.MULTILINE)
    data = []
    for scanner in all_scanners_data:
        if not scanner.strip():
            continue
        data.append(
            [
                Vector(int(c) for c in line.strip().split(","))
                for line in scanner.splitlines()
                if line
            ]
        )
    return data
