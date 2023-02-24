import dearpygui.dearpygui as dpg
import filetype
from PIL import Image
import numpy as np

from app.settings import UserSettings


def preview_if_possible(path, usersettings : UserSettings):
    pn : str = path.name
    print(pn[pn.rfind('.')+1:].lower(), usersettings.text_formats)
    if pn[pn.rfind('.')+1:].lower() in usersettings.text_formats:
        dpg.delete_item('file_preview_text')
        line_limit = usersettings.file_preview_text_line_limit
        contents = ''
        with open(path) as f:
            while line_limit > 0:
                print(line_limit)
                try:
                    line = f.readline()
                except EOFError:
                    break
                contents += line
                line_limit -= 1
            if line_limit == 0:
                contents += '<...>'
        dpg.add_text(contents, label='file_preview_text')

    elif filetype.is_image(str(path)):
        dpg.delete_item('file_preview_texture')

        image = Image.open(path)
        image = image.convert('RGBA')
        w, h = image.size
        k = 526 / h
        w = int(w * k)
        h = int(h * k)

        image = image.resize((w, h))

        image_data = np.asarray(image) / 255
        height, width, channels = image_data.shape
        

        with dpg.texture_registry():
            dpg.add_static_texture(width=width, height=height, default_value=image_data.flatten(), tag="file_preview_texture")
        dpg.add_image("file_preview_texture")
    #elif filetype.is_audio(str(path)):
