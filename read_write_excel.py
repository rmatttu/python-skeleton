import argparse
import datetime
from dataclasses import dataclass, field
from typing import Optional

import openpyxl
from openpyxl.utils import column_index_from_string

__version__ = "0.0.1"


@dataclass
class SimpleArgs(object):
    """Args"""

    source: str


def main():
    """Read/Write excel file"""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument("source", type=str, help="Target excel filename.")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
        help="Show version and exit",
    )
    args = parser.parse_args()  # type: SimpleArgs

    local_timezone = datetime.datetime.now().astimezone().tzinfo
    start_datetime = datetime.datetime.now(local_timezone)

    xl = openpyxl.load_workbook(filename=args.source)
    sheet = xl.active
    cell = sheet["A1"]
    print(type(cell))
    print(cell.value)
    print(sheet["A2"].value)
    print(sheet["A3"].value)
    xl.close()


if __name__ == "__main__":
    main()
