"""log_tool"""

from typing import Optional
import datetime
import logging
import os


def get_log_file_name():
    """Make 'logs' dir and generate log name e.g. 'logs/2021-01-26_10-11-12.123.log'"""
    log_dir = "logs"
    local_timezone = datetime.datetime.now().astimezone().tzinfo
    start_datetime = datetime.datetime.now(local_timezone)
    os.makedirs(log_dir, exist_ok=True)
    filename = os.path.join(
        log_dir, start_datetime.strftime("%Y-%m-%d_%H-%M-%S.%f") + ".log"
    )
    return filename


def setup_logger(log_filename: Optional[str] = None, modname=__name__):
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

    if log_filename:
        fh = logging.FileHandler(log_filename, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
