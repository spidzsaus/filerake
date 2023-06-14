import dearpygui.dearpygui as dpg
import filetype
from PIL import Image
import numpy as np
from pathlib import Path

from app.audio_player_manager import AudioPlayerManager
from core.settings import Settings


def text_preview(path: Path, line_limit: int):
    dpg.delete_item('file_preview_text')
    contents = ''
    try:
        with open(path) as f:
            while line_limit > 0:
                try:
                    line = f.readline()
                except EOFError:
                    break
                contents += line
                line_limit -= 1
            if line_limit == 0:
                contents += '<...>'
    except:
        dpg.add_text("Unable to load text file")
        return
    dpg.add_text(contents, label='file_preview_text')


def image_preview(path: Path):
    dpg.delete_item('file_preview_texture')
    try:
        image = Image.open(path)
        image = image.convert('RGBA')
    except:
        dpg.add_text("Unable to load image file")
        return
    w, h = image.size
    k = 360 / h
    w = int(w * k)
    h = int(h * k)
    image = image.resize((w, h))
    image_data = np.asarray(image) / 255
    height, width, channels = image_data.shape
    with dpg.texture_registry():
        dpg.add_static_texture(width=width, height=height, default_value=image_data.flatten(), tag="file_preview_texture")
    dpg.add_image("file_preview_texture")


def audio_preview(path: Path, audio_player_manager: AudioPlayerManager):
    dpg.delete_item('file_preview_audio_start')
    dpg.delete_item('file_preview_audio_stop')
    
    audio_player_manager.open_audio_player(path)

    def start_callback():
        audio_player_manager.get_audio_player().play()
    def stop_callback():
        audio_player_manager.get_audio_player().stop()
    
    dpg.add_button(label="Play audio file", callback=start_callback, id='file_preview_audio_start')
    dpg.add_button(label="Stop audio file", callback=stop_callback, id='file_preview_audio_stop')


def preview_file(path: Path, settings: Settings, audio_player_manager: AudioPlayerManager):
    if path.suffix[1:] in settings.text_extensions:
        return text_preview(path, settings.file_preview_text_line_limit)
    if filetype.is_image(str(path)):
        return image_preview(path)
    if filetype.is_audio(str(path)):
        return audio_preview(path, audio_player_manager)
    dpg.add_text("Unable to preview file")