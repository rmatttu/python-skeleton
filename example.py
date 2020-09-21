# vim: fileencoding=utf-8

import argparse
import yaml
import logging.config
import datetime
import json
import os

import log_tool

__version__ = '1.0.0'

class ExampleClass(object):
    def __init__(self, value=100):
        self.value = value

    def power(self):
        return self.value * self.value

    def __repr__(self):
        return

    def __str__(self):
        return 'value: {}'.format(self.value)

    @staticmethod
    def lambda_test(exampleObjs):
        values = list(map(lambda x: x.value, exampleObjs))
        return values

class ExampleClassB(ExampleClass):
    def __init__(self, value=100, value2=200):
        super().__init__(value=value)
        self.value2 = value2

    def __str__(self):
        return 'value: {}, value2: {}'.format(self.value, self.value2)

class ExampleList(object):
    def __init__(self, examples):
        self._examples = examples

    def output_file(self):
        extension = '.csv'
        name = 'output_{}{}'.format(self.generate_now_string(), extension)
        fullname = os.path.join('local', name)
        lines = []
        lines.append(', '.join(['a', 'b', 'c']))
        lines.append(', '.join([str(i.value) for i in self._examples]))
        with open(fullname, mode='w') as f:
            f.writelines('\n'.join(lines))
            f.write('\n\n ok.')

    def generate_now_string(self):
        JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
        return datetime.datetime.now(JST).strftime('%Y_%m_%d__%H_%M_%S')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('src', default='src_dir', help='source directory (src_dir)')
    parser.add_argument('dst', default='dst_dir', help='destination directory (dst_dir)')
    parser.add_argument('--foo', default='test', help='optional string foo (test)')
    parser.add_argument('--optional-num', default=5, type=int, help='intのみを受け付けるオプション (5)')
    parser.add_argument('--sw1', action='store_true', help='switch 1, オプションを付けるとsw2はtrue (false)')
    parser.add_argument('--sw2', action='store_false', help='switch 2, オプションを付けるとsw2はfalse (true)')
    parser.add_argument('-i','--inputs', action='append', help='何度も使用できるオプション、例: "-i this -i is -i test"')
    parser.add_argument('-v', '--version', action='version', version=__version__, help='Show version and exit')
    args = parser.parse_args()
    conf = yaml.safe_load(open('conf/local.yml', 'r+', encoding='utf-8'))

    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')
    startDatetime = datetime.datetime.now(JST)
    os.makedirs('logs', exist_ok=True)
    logger = log_tool.setup_logger(os.path.join('logs', 'log.log'))

    # ログ出力
    logger.debug('Starting {}.{} (v{})'.format(__file__, __name__, __version__))
    logger.debug('args: ' + json.dumps(vars(args)))
    logger.log(20, 'info')
    logger.log(30, 'warning')
    logger.log(100, 'test')
    logger.info('info')
    logger.warning('warning')
    logger.debug(args)
    logger.info(conf['settings']['nihongo'])

    # 設定ファイル
    if conf['settings']['bool-test'] == True:
        logger.info(conf['settings']['nihongo'])
        logger.info(str(conf['settings']['int_test']))
        logger.info(str(conf['settings']['int_test']).zfill(4))

    # 継承
    b = ExampleClassB()
    logger.debug('Print ExampleClassB.')
    logger.debug(b)

    exampleObjs = [
        ExampleClassB(value=1),
        ExampleClassB(value=2),
        ExampleClassB(value=3),
    ]
    values = ExampleClass.lambda_test(exampleObjs)
    logger.debug('Print values: ' + str(values))

    # リスト内記法、map、filter
    numbers1 = [i for i in range(10)]
    numbersStr = [str(i) for i in range(10)]
    logger.debug('numbers1:        ' + str(numbers1))
    logger.debug('numbersStr:      ' + str(numbersStr))

    tests = [ExampleClass(i) for i in range(10)]
    testsPow = [str(i.power()) for i in tests]
    logger.debug('testsPow:        ' + ', '.join(testsPow))

    testsList = [str(i) for i in tests]
    testsMap = map(lambda i: str(i.value), tests)
    testsFilter = list(filter(lambda i: i.value % 2 == 0, tests))
    logger.debug('testsList:       ' + ', '.join(testsList))
    logger.debug('testsMap:        ' + ', '.join(testsMap))

    testsFilterStr = map(lambda i: str(i.value), testsFilter)
    testsFilterList = [str(i) for i in tests if i.value % 2 == 0]
    logger.debug('testsFilterStr:  ' + ', '.join(testsFilterStr))
    logger.debug('testsFilterList: ' + ', '.join(testsFilterList))

    # ファイル書き込み
    exampleList = ExampleList(tests)
    exampleList.output_file()


if __name__ == '__main__':
    main()
