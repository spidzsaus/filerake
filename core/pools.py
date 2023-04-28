from .warnings import *

from pathlib import Path
from random import randint
import shutil
import re


eventDelete = object()


class PoolAction:
    MOVE = "MOVE"
    COPY = "COPY"


class Pool:
    name : str
    path : Path
    pattern : re.Pattern
    action : PoolAction
    
    def __init__(self, name=None, path=None, pattern=None, action=PoolAction.MOVE):
        if path is None:
            path = ""
        if pattern is None:
            pattern = ""
        self.name = name
        self.path = Path(path)
        self.pattern = re.compile(pattern)
        self.action = action

    @classmethod
    def from_json(cls, dic: dict):
        new = cls()
        new.name = dic["name"]
        new.path = Path(dic["path"])
        new.pattern = re.compile(dic["pattern"], re.UNICODE)
        new.action = dic["action"]
        return new

    def to_json(self):
        dic = {}
        dic["name"] = self.name
        dic["path"] = str(self.path)
        dic["pattern"] = self.pattern.pattern
        dic["action"] = self.action
        return dic
    
    def send(self, filepath: Path):
        warnings = set()
        name = filepath.name
        if (self.path / name).exists():
            name = name[:name.rfind('.')] + str(randint(0, 999999)) + name[name.rfind('.'):]
            warn = FileExistsWarning("file exists, added random suffix", filepath=filepath, name=name)
            warnings.add(warn)
        newpath = self.path / name
        match self.action:
            case PoolAction.MOVE:
                shutil.move(filepath, newpath)
            case PoolAction.COPY:
                shutil.copyfile(filepath, newpath)

class IgnorePool(Pool):
    @classmethod
    def from_json(cls, dic: dict):
        return NotImplemented

    def to_json(self):
        return NotImplemented
    
    def send(self, filepath: Path):
        pass