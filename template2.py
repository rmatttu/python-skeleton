"""template2"""

import argparse
import dataclasses
import datetime
import glob
import json
import logging
import os
import pathlib
import sys
import typing

import system_loader

__version__ = "0.0.0"


@dataclasses.dataclass
class SimpleArgs(object):
    """Args"""
    src: str
    dst: str
    foo: str
    optional_num: int
    sw1: bool
    sw2: bool
    inputs: list


def simple_setup_logger(logFileName: typing.Optional[str] = None, modname=__name__):
    """Setup simple logger"""
    logger = logging.getLogger(modname)
    logger.setLevel(logging.DEBUG)
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(
        "%(asctime)s.%(msecs)03d\t%(levelname)s\t%(message)s", datefmt
    )

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    if logFileName:
        fh = logging.FileHandler(logFileName, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def main():
    """Sample code"""
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        "src", default="src_dir", type=str, help="source directory (src_dir)"
    )
    parser.add_argument(
        "dst", default="dst_dir", type=str, help="destination directory (dst_dir)"
    )
    parser.add_argument(
        "--foo", default="test", type=str, help="optional string foo (test)"
    )
    parser.add_argument(
        "--optional-num", default=5, type=int, help="intのみを受け付けるオプション (5)"
    )
    parser.add_argument(
        "--sw1", action="store_true", help="switch 1, オプションを付けるとsw2はtrue (false)"
    )
    parser.add_argument(
        "--sw2", action="store_false", help="switch 2, オプションを付けるとsw2はfalse (true)"
    )
    parser.add_argument(
        "-i",
        "--inputs",
        action="append",
        help='何度も使用できるオプション、例: "-i this -i is -i test"',
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
        help="Show version and exit",
    )
    args = parser.parse_args()  # type: system_loader.SimpleArgs

    local_timezone = datetime.datetime.now().astimezone().tzinfo
    start_datetime = datetime.datetime.now(local_timezone)

    logger: logging.Logger = None
    logger = simple_setup_logger()

    # File logger
    # os.makedirs('logs', exist_ok=True)
    # logger = simple_setup_logger(os.path.join('logs', 'log.log'))

    logger.debug(
        "\t".join(["Starting", str(__file__), str(__name__), str(__version__)])
    )
    logger.debug("\t".join(["args", json.dumps(vars(args), ensure_ascii=False)]))

    mypath = pathlib.Path("this/is/test/path")
    mypath = mypath.joinpath(str(mypath), "sub-dir")
    print(str(mypath), file=sys.stderr)

    def close(code: int):
        processing_time = datetime.datetime.now(local_timezone) - start_datetime
        logger.debug(
            "\t".join(
                [
                    "processingTime",
                    str(processing_time.total_seconds()) + "s",
                    str(processing_time),
                ]
            )
        )
        exit(code)

    # 終了
    close(0)


if __name__ == "__main__":
    main()
