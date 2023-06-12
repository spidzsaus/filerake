from __future__ import annotations

import enum
from pathlib import Path
import re
import os
import datetime
import shutil
from send2trash import send2trash
from typing import TYPE_CHECKING

from app.utils import filename_format


class PileMode(enum.Enum):
    MOVE_TO_DIR = "MOVE_TO_DIR"
    COPY_TO_DIR = "COPY_TO_DIR"
    DELETE = "DELETE"
    DELETE_PERMANENTLY = "DELETE_PERMANENTLY"
    IGNORE = "IGNORE"

class Pile:
    name: str
    mode: PileMode
    path: Path | None
    pattern: re.Pattern
    hotkey: list[str] | None
    file_rename_format: str
    always_rename_files: bool

    def __init__(
        self, 
        name: str, 
        mode: PileMode, 
        path: Path | None = None,
        pattern: re.Pattern | None = None,
        hotkey: list[str] | None = None,
        file_rename_format: str | None = None,
        always_rename_files: bool = False
    ):
        self.name = name
        self.mode = mode
        self.path = path
        self.pattern = pattern
        self.hotkey = hotkey
        self.file_rename_format = (
            file_rename_format
            if file_rename_format else
            r'{name}{extension} from {dir}'
        )
        self.always_rename_files = always_rename_files
    
    def _destination_filepath(self, source_filepath: Path) -> Path:
        if self.path is None:
            return source_filepath
        filename = source_filepath.name
        newpath = self.path / filename
        if newpath.exists() or self.always_rename_files:
            timestamp = datetime.datetime.now()
            newpath = filename_format(
                filepath=newpath,
                format=self.file_rename_format, 
                timestamp=timestamp
            )
        return newpath

    def recieve(self, file: Path):
        match self.mode:
            case PileMode.COPY_TO_DIR:
                shutil.copyfile(file, self._destination_filepath(file))
            case PileMode.MOVE_TO_DIR:
                shutil.move(file, self._destination_filepath(file))
            case PileMode.DELETE:
                send2trash(file)
            case PileMode.DELETE_PERMANENTLY:
                os.remove(file)
            case PileMode.IGNORE:
                pass
        
                

    @classmethod
    def from_json(cls, obj: dict) -> Pile:
        new = cls(
            name=obj['name'],
            mode=PileMode(obj['mode']),
            path=Path(obj['path']) if 'path' in obj else None,
            pattern=re.compile(obj['pattern'], re.UNICODE) if 'pattern' in obj else None,
            hotkey=obj['hotkey'] if 'hotkey' in obj else None,
            file_rename_format=obj['file_rename_format'],
            always_rename_files=obj['always_rename_files']
        )
        return new
    
    def to_json(self) -> dict:
        obj = {}
        obj['name'] = self.name
        obj['mode'] = self.mode
        if self.path:
            obj['path'] = str(self.path)
        if self.pattern:
            obj['pattern'] = self.pattern.pattern
        if self.hotkey:
            obj['hotkey'] = self.hotkey
        obj['file_rename_format'] = self.file_rename_format
        obj['always_rename_files'] = self.always_rename_files
        return obj