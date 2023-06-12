from app.raking_piles import Pile

class Settings:
    piles: list[Pile]
    text_extensions: list[str]
    file_preview_text_line_limit: int

    def __init__(
        self,
        piles: list[Pile],
        text_extensions: list[str],
        file_preview_text_line_limit: int
    ):
        self.piles = piles
        self.text_extensions = text_extensions
        self.file_preview_text_line_limit = file_preview_text_line_limit

DEFAULT_SETTINGS = Settings(
    piles=[],
    text_extensions=['txt', 'md', 'html', 'py', 'cpp', 'json'],
    file_preview_text_line_limit=100
)
