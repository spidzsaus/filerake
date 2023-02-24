from .warnings import *

from pathlib import Path
from random import randint
import shutil
import re


class Pool:
    name : str
    path : Path
    pattern : re.Pattern

    @classmethod
    def from_json(cls, dic: dict):
        new = cls()
        
        new.name = dic["name"]
        new.path = Path(dic["path"])
        new.pattern = re.compile(dic["pattern"], re.UNICODE)
        return new
    
    def send(self, filepath: Path):
        warnings = set()
        name = filepath.name
        if (self.path / name).exists():
            name = name + str(randint(0, 999999))
            warn = FileExistsWarning("file exists, added random suffix", filepath=filepath, name=name)
            warnings.add(warn)
        newpath = self.path / name
        shutil.move(str(filepath), str(newpath))
        