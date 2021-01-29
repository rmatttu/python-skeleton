import dataclasses
import pathlib
import os

import yaml

@dataclasses.dataclass
class Log:
    output_file: bool

@dataclasses.dataclass
class Settings:
    nihongo: str
    bool_test: bool
    int_test: int

@dataclasses.dataclass
class Conf:
    log: Log
    settings: Settings

@dataclasses.dataclass
class Loader:
    path: pathlib.Path = dataclasses.field(default=pathlib.Path(os.path.join('conf', 'local.yml')))
    encoding: str = dataclasses.field(default='utf-8')

    def load(self):
        confDict = {}
        source = yaml.safe_load(open(str(self.path), 'r+', encoding=self.encoding))
        confDict['log'] = Settings(**source['log'])
        confDict['settings'] = Settings(**source['settings'])
        return Conf(**confDict)

@dataclasses.dataclass
class SampleArgs(object):
    src: str
    dst: str
    foo: str
    optional_num: int
    sw1: bool
    sw2: bool
    inputs: list
