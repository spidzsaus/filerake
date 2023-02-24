from tkinter import filedialog
import dearpygui.dearpygui as dpg

from app.settings import UserSettings

__searchPath__ = 'C:/'
__settings__ = UserSettings('config/settings.json')

def select_path(sender, app_data):
    dir_input = filedialog.askdirectory()
    if not dir_input: return
    __searchPath__ = dir_input
    dpg.set_value('main label',
                  f"Sorting path: {__searchPath__}")

dpg.create_context()
dpg.create_viewport(title="SortMe!")
dpg.setup_dearpygui()

with dpg.font_registry ():
    with dpg.font("assets\\fonts\\juliamono\\JuliaMono-Regular.ttf", 18, default_font=True, tag="cyr"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

dpg.bind_font("cyr")

with dpg.window(tag="window", label="Example Window"):
    dpg.add_text(f"Sorting path: {__searchPath__}", id='main label')
    dpg.add_button(label="Change directory", callback=select_path)

dpg.show_viewport()
dpg.set_primary_window("window", True)
dpg.start_dearpygui()
dpg.destroy_context()