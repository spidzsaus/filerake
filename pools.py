from context import __SuggestionTable__
from pathlib import Path
from random import randint
from core.warnings import *

class Pool:
    name : str
    path : Path

    @classmethod
    def from_json(cls, dic: dict):
        new = cls()
        
        new.name = dic["name"]
        new.path = Path(dic["path"])
        __SuggestionTable__.add_rule(new, dic["pattern"])
        return new
    
    def send(self, filepath: Path):
        warnings = set()
        name = filepath.name
        if (self.path / name).exists():
            name = name + str(randint(0, 999999))
            warn = FileExistsWarning("file exists, added random suffix", filepath=filepath, name=name)
            warnings.add(warn)
        filepath.rename(self.path / name)
        