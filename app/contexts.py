import audioplayer
from pathlib import Path

from core.suggestions import SuggestionTable

from .raking_session import RakingSession
from .settings import UserSettings

class Context:
    def __init__(self, init_path="C:/", settings_file="config/settings.json"):
        self.current_path = Path(init_path)
        self.settings = UserSettings(settings_file)
        self.session = None
        self.audioplayer = None
        self.suggestion_table = SuggestionTable()
        self.suggestion_table.feed_pools(self.settings.pools)
        self._tmp_poolstable = {}
        self._tmp_ptc = 0
    
    def set_path(self, path):
        self.current_path = Path(path)

    def get_path(self):
        return self.current_path

    def get_settings(self):
        return self.settings

    def get_session(self):
        return self.session

    def start_session(self):
        self.session = RakingSession(self.get_path(),
                                     self)
    
    def get_pools(self):
        return self.get_settings().pools[:]
    
    def get_pool(self, idx):
        if idx in self._tmp_poolstable:
            return self._tmp_poolstable[idx]
    
    def register_pool(self, pool):
        idx = self._tmp_ptc
        self._tmp_poolstable[idx] = pool
        self._tmp_ptc += 1
        return idx
    
    def open_audio_player(self, path):
        self.audioplayer = audioplayer.AudioPlayer(str(path))

    def get_audio_player(self):
        return self.audioplayer

    def close_audio_player(self):
        if self.audioplayer is not None:
            self.audioplayer.close()
    
    def clear_pools_table(self):
        self._tmp_poolstable.clear()
        self._tmp_ptc = 0
    
    def update_settings(self):
        if self.session is not None:
            self.session.settings = self.settings
        self.suggestion_table.feed_pools(self.settings.pools)
    
    def get_suggestion_table(self):
        return self.suggestion_table