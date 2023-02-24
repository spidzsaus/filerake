from tkinter import filedialog
import dearpygui.dearpygui as dpg
from pathlib import Path
import audioplayer
import os

from app.settings import UserSettings
from app.raking_session import RakingSession, RakingStep
from app.preview import preview_if_possible
from app.settings_window import open_settings_window
from core.pools import *

class Context:
    __searchPath__ = Path('C:/')
    __settings__ = UserSettings('config/settings.json')
    __session__ : RakingSession = None
    __tempPoolsTable__ = {-1: IgnorePool()}
    __audioPlayer__ : audioplayer.AudioPlayer = None
    __recycleBin__ = []


def select_path(sender, app_data):
    dir_input = filedialog.askdirectory()
    if not dir_input: return
    Context.__searchPath__ = Path(dir_input)
    dpg.set_value('main label',
                  f"Sorting path: {Context.__searchPath__}")

def start_raking(sender, app_data):
    Context.__session__ = RakingSession(Context.__searchPath__, Context.__settings__)
    Context.__recycleBin__ = []
    next_raking(..., ...)

def next_raking(sender, app_data):
    if Context.__audioPlayer__ is not None:
        Context.__audioPlayer__.close()

    if sender is not Ellipsis:
        idx = int(sender[len('POOL'):])
        if idx <= -2:
            pool = None
        else:
            pool = Context.__tempPoolsTable__[idx]
    else:
        idx = None
        pool = None
    if idx == -2:
        Context.__recycleBin__.append(Context.__session__.prev_file)
    if idx == -3:
        dir_input = filedialog.askdirectory()
        if dir_input: 
            tmp = Pool()
            tmp.path = Path(dir_input)
            tmp.send(Context.__session__.prev_file)
    step = Context.__session__.next(pool)
    dpg.delete_item('raking')
    if step:
        count = 0
        Context.__tempPoolsTable__ = {-1: IgnorePool()}
        with dpg.child_window(parent='window', tag="raking", label="Raking"):
            with dpg.group(horizontal=True):
                with dpg.child_window(width=1000): 
                    dpg.add_text(f'Reviewing {step.file.name}')
                    dpg.add_loading_indicator(tag="preview_loading")
                    with dpg.child_window(border=False):
                        preview_if_possible(step.file, Context)
                    dpg.delete_item("preview_loading")
                with dpg.group():
                    with dpg.child_window(height=200, border=False):
                        if step.suggestions:
                            dpg.add_text('Suggested pools:')
                            for sgst in step.suggestions:
                                dpg.add_button(label=sgst.name, callback=next_raking, tag=f"POOL{count}",
                                               width=-1)
                                dpg.bind_item_theme(dpg.last_item(), "theme_suggestion")
                                Context.__tempPoolsTable__[count] = sgst
                                count += 1
                            dpg.add_separator()
                        else:
                            dpg.add_text("No pool suggestions")
                    with dpg.child_window(height=400, border=False):
                        for pool in step.pools:
                            dpg.add_button(label=pool.name, callback=next_raking, tag=f"POOL{count}",
                                           width=-1)
                            dpg.bind_item_theme(dpg.last_item(), "theme_pool")
                            Context.__tempPoolsTable__[count] = pool
                            count += 1
                    dpg.add_separator()
                    dpg.add_button(label='Ignore', callback=next_raking, tag=f"POOL-1",
                                   width=-1)
                    dpg.add_button(label='Choose location', callback=next_raking, tag=f"POOL-3",
                                   width=-1)
                    dpg.add_spacer(height=10)

                    dpg.add_button(label='Delete', callback=next_raking, tag=f"POOL-2",
                                   width=-1)
                    dpg.bind_item_theme(dpg.last_item(), "theme_red")
    else:
        with dpg.child_window(parent='window', tag="raking", label="Raking"):
            dpg.add_text('All sorted!')
            if Context.__recycleBin__:
                dpg.add_text("You've marked following files for deletion:")
                for file in Context.__recycleBin__:
                    dpg.add_checkbox(label=file.name, tag=str(file),
                                    default_value=True)
                dpg.add_text("Are you sure you want to delete them?")
                dpg.add_text("Unmark the files you want to keep")

                def deletion_callback():
                    for file in Context.__recycleBin__:
                        if dpg.get_value(str(file)):
                            os.remove(str(file))
                    dpg.delete_item('raking')
                dpg.add_button(label="Delete all marked files", callback=deletion_callback)
                dpg.bind_item_theme(dpg.last_item(), "theme_red")



dpg.create_context()
dpg.create_viewport(title="spidz.FileRake")
dpg.setup_dearpygui()

with dpg.font_registry ():
    with dpg.font("assets\\fonts\\juliamono\\JuliaMono-Regular.ttf", 18, default_font=True, tag="cyr"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

dpg.bind_font("cyr")

with dpg.theme(tag="theme_red"):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [172, 59, 80])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [215, 76, 102])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [241, 106, 132])

with dpg.theme(tag="theme_suggestion"):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [142, 226, 240])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [116, 235, 255])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [97, 189, 204])
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 10)
        dpg.add_theme_color(dpg.mvThemeCol_Text, [24, 32, 24])

with dpg.theme(tag="theme_pool"):
    with dpg.theme_component(dpg.mvButton):
        dpg.add_theme_color(dpg.mvThemeCol_Button, [127, 179, 159])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [114, 185, 158])
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [124, 205, 174])
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 10)
        dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 10)
        dpg.add_theme_color(dpg.mvThemeCol_Text, [24, 32, 24])

with dpg.window(tag="window", label="Example Window"):
    with dpg.group(horizontal=True):
        dpg.add_button(label="Start raking", callback=start_raking)
        dpg.add_button(label="Change directory", callback=select_path)
        dpg.add_button(label="Settings", callback=lambda : open_settings_window(Context))
    dpg.add_text(f"Sorting path: {Context.__searchPath__}", tag='main label')
    

dpg.set_viewport_large_icon("assets/icon.ico")
dpg.set_viewport_small_icon("assets/icon.ico")

dpg.show_viewport()
dpg.set_primary_window("window", True)
dpg.start_dearpygui()
dpg.destroy_context()