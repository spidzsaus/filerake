import dearpygui.dearpygui as dpg
import filetype
from PIL import Image
import numpy as np

def preview_if_possible(path):
    if filetype.is_image(str(path)):
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
