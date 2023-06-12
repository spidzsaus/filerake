from pathlib import Path

from app.raking_piles import Pile


class Session:
    changes: dict[Path, Pile]

    def record(self, file: Path, pile: Pile):
        self.changes[file] = pile

    def commit(self, mask: list[Path] | None = None):
        changes = self.changes
        for key, value in changes.items():
            if mask and key not in mask: continue
            value.recieve(key)
