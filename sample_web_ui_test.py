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
from selenium.webdriver.remote import webelement
import chromedriver_binary # Adds chromedriver binary to path

import log_tool
import system_loader

__version__ = '0.0.1'

def main():
    """ sample_web_test
    """
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('-v', '--version', action='version', version=__version__, help='Show version and exit')
    args = parser.parse_args() # type: system_loader.SampleArgs
    conf = system_loader.Loader().load()

    localTimeZone = datetime.datetime.now().astimezone().tzinfo
    startDatetime = datetime.datetime.now(localTimeZone)

    logger: logging.Logger = None
    if conf.log.output_file:
        os.makedirs('logs', exist_ok=True)
        logger = log_tool.setup_logger(os.path.join('logs', 'log.log'))
        # launchly log
        # logger = log_tool.setup_logger(log_tool.get_log_file_name())
    else:
        logger = log_tool.setup_logger()

    logger.debug('\t'.join(['Starting',str(__file__), str(__name__), str(__version__)]))
    logger.debug('\t'.join(['args', json.dumps(vars(args), ensure_ascii=False)]))

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-infobars')
    # options.add_argument('--kiosk') # Full screen
    # options.add_argument('--user-data-dir=' + './test/') # Save browser data
    driver = webdriver.Chrome(chromedriver_binary.chromedriver_filename, chrome_options=options)

    def wait():
        time.sleep(3)

    def close(code: int):
        processingTime = datetime.datetime.now(localTimeZone) - startDatetime
        logger.debug('\t'.join(['processingTime', str(processingTime.total_seconds()) + 's', str(processingTime)]))
        exit(code)

    try:
        driver.get('https://www.google.com/')
        el: webelement.WebElement = driver.find_element_by_class_name('gLFyf')
        el.send_keys('search word')
        wait()
        el: webelement.WebElement = driver.find_element_by_class_name('MV3Tnb')
        text = el.text
        logger.debug(text)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        # fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error('\t'.join([str(type(e)), exc_tb.tb_frame.f_code.co_filename, f'line {str(exc_tb.tb_lineno)}', str(e)]))
        driver.close()
        close(1)
    close(0)

if __name__ == '__main__':
    main()
