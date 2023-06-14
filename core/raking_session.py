from pathlib import Path
from core.raking_piles import Pile


class Session:
    changes: dict[Path, Pile]
    root: Path
    cursor: int

    def __init__(self, root: Path, is_reversed: bool = False):
        self.root = root
        self.files = [file for file in root.iterdir() if file.is_file()]
        self._files_len = len(self.files)
        self.is_reversed = is_reversed
        self.cursor = (self._files_len - 1) if is_reversed else 0
    
    def next_file(self):
        self.cursor += -1 if self.is_reversed else +1
        if not (0 <= self.cursor < self._files_len):
            return None
        return self.files[self.cursor]

    def previous_file(self):
        self.cursor += +1 if self.is_reversed else -1
        if not (0 <= self.cursor < self._files_len):
            return None
        return self.files[self.cursor]

    def record(self, file: Path, pile: Pile):
        self.changes[file] = pile

    def commit(self, mask: list[Path] | None = None):
        changes = self.changes
        for key, value in changes.items():
            if mask and key not in mask: continue
            value.recieve(key)
