from pathlib import Path
from core.pools import Pool
from .settings import UserSettings

class RakingStep:
    def __init__(self, file, suggestions, pools):
        self.file = file
        self.suggestions = suggestions
        self.pools = pools

class RakingSession:
    path : Path
    settings : UserSettings

    def __init__(self, path : Path, settings : UserSettings):
        self.path = path
        self.settings = settings
        self.pile = (f for f in path.iterdir() if f.is_file())
        self.prev_file = None
    
    def next(self, pool : Pool=None):
        if self.prev_file is not None and pool is not None:
            pool.send(self.prev_file)

        try:
            file = next(self.pile)
        except StopIteration:
            return None
        
        name = file.name
        suggestions = self.settings.suggestion_table.suggest(name)
        pools = self.settings.pools

        self.prev_file = file
        return RakingStep(file, suggestions, pools)
