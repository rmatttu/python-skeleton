from typing import Optional
import datetime
import logging
import os


def get_log_file_name():
    """Make 'logs' dir and generate log name e.g. 'logs/2021-01-26_10-11-12.123.log'"""
    logDir = "logs"
    localTimeZone = datetime.datetime.now().astimezone().tzinfo
    startDatetime = datetime.datetime.now(localTimeZone)
    os.makedirs(logDir, exist_ok=True)
    filename = os.path.join(
        logDir, startDatetime.strftime("%Y-%m-%d_%H-%M-%S.%f") + ".log"
    )
    return filename


def setup_logger(logFileName: Optional[str] = None, modname=__name__):
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
