"""template1"""

import logging
import sys

__version__ = "0.0.0"


def setup_logger(modname=__name__):
    """setup logger"""
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
    return logger


def main():
    """simple_main"""
    logger = setup_logger()

    try:
        devide_zero = 1230 / 0
        logger.debug(str(devide_zero))
    except Exception as ex:
        logger.error("\t".join([str(type(ex)), str(ex)]))
        # traceback.print_exc()
        # exc_type, exc_obj, exc_tb = sys.exc_info()
        _, _, exc_tb = sys.exc_info()
        logger.error(
            "\t".join(
                [
                    str(type(ex)),
                    f"{exc_tb.tb_frame.f_code.co_filename}:{str(exc_tb.tb_lineno)}",
                    str(ex),
                ]
            )
        )


if __name__ == "__main__":
    main()
