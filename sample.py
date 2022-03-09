import argparse
import dataclasses
import datetime
import glob
import json
import logging
import os
import pathlib
import typing

import yaml

import log_tool
import system_loader

__version__ = "1.4.0"


class ExampleClass(object):
    def __init__(self, value=100):
        self.value = value

    def power(self):
        return self.value * self.value

    def __str__(self):
        return "value: {}".format(self.value)

    @staticmethod
    def lambda_test(exampleObjs):
        values = list(map(lambda x: x.value, exampleObjs))
        return values


class ExampleClassB(ExampleClass):
    def __init__(self, value=100, value2=200):
        super().__init__(value=value)
        self.value2 = value2

    def __str__(self):
        return "value: {}, value2: {}".format(self.value, self.value2)


class ExampleList(object):
    def __init__(self, examples):
        self._examples = examples

    def output_file(self):
        extension = ".csv"
        name = "output_{}{}".format(self.generate_now_string(), extension)
        fullname = os.path.join("local", name)
        lines = []
        lines.append(", ".join(["a", "b", "c"]))
        lines.append(", ".join([str(i.value) for i in self._examples]))
        with open(fullname, mode="w", encoding="utf-8") as f:
            f.writelines("\n".join(lines))
            f.write("\n\n ok.")

    def generate_now_string(self):
        JST = datetime.timezone(datetime.timedelta(hours=+9), "JST")
        return datetime.datetime.now(JST).strftime("%Y_%m_%d__%H_%M_%S")


@dataclasses.dataclass
class FileStat:
    path: pathlib.Path
    stat: os.stat_result = dataclasses.field(init=False)

    def __post_init__(self):
        self.stat = os.stat(self.path)


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
    args = parser.parse_args()  # type: system_loader.SampleArgs
    conf = system_loader.Loader().load()

    localTimeZone = datetime.datetime.now().astimezone().tzinfo
    startDatetime = datetime.datetime.now(localTimeZone)

    logger: logging.Logger = None
    if conf.log.output_file:
        os.makedirs("logs", exist_ok=True)
        logger = log_tool.setup_logger(os.path.join("logs", "log.log"))
        # launchly log
        # logger = log_tool.setup_logger(log_tool.get_log_file_name())
    else:
        logger = log_tool.setup_logger()

    logger.debug(
        "\t".join(["Starting", str(__file__), str(__name__), str(__version__)])
    )
    logger.debug("\t".join(["args", json.dumps(vars(args), ensure_ascii=False)]))

    def close(code: int):
        processingTime = datetime.datetime.now(localTimeZone) - startDatetime
        logger.debug(
            "\t".join(
                [
                    "processingTime",
                    str(processingTime.total_seconds()) + "s",
                    str(processingTime),
                ]
            )
        )
        exit(code)

    # ログ出力
    logger.log(20, "info")
    logger.log(30, "warning")
    logger.log(100, "test")
    logger.info("info")
    logger.warning("warning")
    logger.debug(args)
    logger.info(conf.settings.nihongo)

    # 設定ファイル
    if conf.settings.bool_test == True:
        logger.info(conf.settings.nihongo)
        logger.info(str(conf.settings.int_test))
        logger.info(str(conf.settings.int_test))
        logger.info(str(conf.settings.int_test).zfill(4))

    # 継承
    b = ExampleClassB()
    logger.debug("Print ExampleClassB.")
    logger.debug(b)

    exampleObjs = [
        ExampleClassB(value=1),
        ExampleClassB(value=2),
        ExampleClassB(value=3),
    ]
    values = ExampleClass.lambda_test(exampleObjs)
    logger.debug(f"Print values: {str(values)}")

    # リスト内記法、map、filter
    numbers1 = [i for i in range(10)]
    numbersStr = [str(i) for i in range(10)]
    logger.debug(f"numbers1:        {str(numbers1)}")
    logger.debug(f"numbersStr:      {str(numbersStr)}")

    tests = [ExampleClass(i) for i in range(10)]
    testsPow = [str(i.power()) for i in tests]
    logger.debug(f"testsPow:        {', '.join(testsPow)}")

    testsList = [str(i) for i in tests]
    testsMap = map(lambda i: str(i.value), tests)
    testsFilter = list(filter(lambda i: i.value % 2 == 0, tests))
    logger.debug(f"testsList:       {', '.join(testsList)}")
    logger.debug(f"testsMap:        {', '.join(testsMap)}")

    testsFilterStr = map(lambda i: str(i.value), testsFilter)
    testsFilterList = [str(i) for i in tests if i.value % 2 == 0]
    logger.debug(f"testsFilterStr:  {', '.join(testsFilterStr)}")
    logger.debug(f"testsFilterList: {', '.join(testsFilterList)}")

    # ファイル書き込み
    exampleList = ExampleList(tests)
    exampleList.output_file()

    # ファイル読み込み
    lines = []
    with open("local/input.txt", "r+", encoding="utf-8") as reader:
        lines = reader.readlines()
    for index, item in enumerate(lines):
        line = item.replace("\r", "").replace("\n", "")
        lineNo = index + 1
        if not line:
            logger.warning("\t".join(["emptyLine", str(lineNo)]))
            continue
        logger.debug("\t".join(["data", str(lineNo), line]))

    # ファイルリスト取得・更新日時ソート
    targetDir = pathlib.Path("./")
    search = "*.py"
    files = glob.glob(str(targetDir.joinpath(search)))
    fileStats = [FileStat(pathlib.Path(i)) for i in files]
    logger.debug("\n".join([str(i) for i in fileStats]))

    print("")
    print("---Default order---")
    print("\n".join([str(i.path) for i in fileStats]))

    # 破壊的（updatedAtの順序が変更される）
    updatedAt = list(fileStats)
    updatedAt.sort(key=lambda i: i.stat.st_mtime)
    print("")
    print("---Order by updated at---")
    print("\n".join([str(i.path) for i in updatedAt]))

    # 非破壊的（元にしたリストの順序は変更されない）
    createdAt = sorted(fileStats, key=lambda i: i.stat.st_ctime)
    print("")
    print("---Order by created at---")
    print("\n".join([str(i.path) for i in createdAt]))

    # 終了
    close(0)


if __name__ == "__main__":
    main()
