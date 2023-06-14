from audioplayer import AudioPlayer


class AudioPlayerManager:
    audioplayer: AudioPlayer | None

    def __init__(self) -> None:
        self.audioplayer = None

    def open_audio_player(self, path):
        self.audioplayer = AudioPlayer(str(path))

    def get_audio_player(self) -> AudioPlayer:
        return self.audioplayer

    def close_audio_player(self):
        if self.audioplayer is not None:
            self.audioplayer.close()