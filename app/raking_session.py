from pathlib import Path
from core.pools import Pool, eventDelete
from .settings import UserSettings

rsIdle = object()
rsActive = object()
rsStopped = object()

class RakingStep:
    @classmethod
    def running_step(cls, file, suggestions):
        new = cls()
        new.is_running = True
        new.file = file
        new.suggestions = suggestions
        return new

    @classmethod
    def last_step(cls, recycle_bin):
        new = cls()
        new.is_running = False
        new.recycle_bin = recycle_bin
        return new

class RakingSession:
    path : Path
    settings : UserSettings

    def __init__(self, path : Path, context):
        self.path = path
        self.context = context
        self.pile = (f for f in path.iterdir() if f.is_file())
        self.recycle_bin = []
        self.current_file = None
        self.prev_file = None
        self.state = rsActive
    
    def finish(self):
        self.state = rsStopped
        self.current_file = None
        self.prev_file = None
    
    def move_to_bin(self, path):
        self.recycle_bin.append(path)
    
    def current_step(self):
        if self.state is rsActive:
            name = self.current_file.name
            suggestions = self.context.get_suggestion_table().suggest(name)
            return RakingStep.running_step(self.current_file, suggestions)
        elif self.state is rsStopped:
            return RakingStep.last_step(self.recycle_bin)
    
    def handle(self, pool):
        if pool is eventDelete:
            self.move_to_bin(self.current_file)
            return
        if self.current_file is not None and pool is not None:
            pool.send(self.current_file)
            return

    def next(self):
        try:
            file = next(self.pile)
            self.prev_file = self.current_file
            self.current_file = file
            return True
        except StopIteration:
            self.finish()
            return False
