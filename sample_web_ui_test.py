import argparse
import dataclasses
import datetime
import json
import logging
import os
import pathlib
import sys
import time
import typing

from selenium import webdriver
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.remote import webelement
from webdriver_manager.chrome import ChromeDriverManager

__version__ = "0.0.1"


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


def simple_setup_logger(log_filename: typing.Optional[str] = None, modname=__name__):
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

    if log_filename:
        fh = logging.FileHandler(log_filename, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger


def main():
    """main"""
    parser = argparse.ArgumentParser(description=main.__doc__)
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

    logger: logging.Logger = None
    logger = simple_setup_logger(None)

    logger.debug(
        "\t".join(["Starting", str(__file__), str(__name__), str(__version__)])
    )
    logger.debug("\t".join(["args", json.dumps(vars(args), ensure_ascii=False)]))

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-infobars")
    # options.add_argument('--kiosk') # Full screen
    # options.add_argument('--user-data-dir=' + './test/') # Save browser data
    caps = desired_capabilities.DesiredCapabilities.CHROME.copy()
    caps["goog:loggingPrefs"] = {"performance": "ALL"}  # enable performance logs
    driver = webdriver.Chrome(
        ChromeDriverManager().install(),
        chrome_options=options,
        desired_capabilities=caps,
    )

    def wait():
        time.sleep(3)

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

    try:
        driver.get("https://www.google.com/")
        el: webelement.WebElement = driver.find_element(By.CLASS_NAME, "gLFyf")
        el.send_keys("search word")
        wait()
        el: webelement.WebElement = driver.find_element(By.CLASS_NAME, "MV3Tnb")
        text = el.text
        logger.debug(text)
    except Exception as ex:
        _, _, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error(
            "\t".join(
                [
                    str(type(ex)),
                    exc_tb.tb_frame.f_code.co_filename,
                    f"line {str(exc_tb.tb_lineno)}",
                    str(ex),
                ]
            )
        )
        driver.close()
        close(1)
    close(0)


if __name__ == "__main__":
    main()
