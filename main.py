from tkinter import filedialog
import dearpygui.dearpygui as dpg
from pathlib import Path
import audioplayer
import os
import sys
import subprocess

from app.settings import UserSettings
from app.raking_session import RakingSession, RakingStep
from app.preview import preview_if_possible
from app.settings_window import open_settings_window
from app.contexts import Context
from core.pools import *

if not os.path.exists("config/settings.json"):
    os.makedirs("config", exist_ok=True)
    UserSettings("config/settings.json").write()

if sys.platform == 'win32':
    FILEOPENER = ['explorer',  '/select,']
elif sys.platform == 'darwin':
    FILEOPENER = ['open', '-R']

CONTEXT = Context()

def select_path():
    dir_input = filedialog.askdirectory()
    if not dir_input: return
    CONTEXT.set_path(dir_input)
    dpg.set_value('main label',
                  f"Sorting path: {CONTEXT.get_path()}")

def start_raking(sender):
    CONTEXT.start_session()
    CONTEXT.session.next()
    update_raking(sender)

def update_raking(sender):
    CONTEXT.close_audio_player()
    session = CONTEXT.get_session()
    if sender.startswith("POOL"):
        idx = int(sender[len('POOL'):])
        session.handle(CONTEXT.get_pool(idx))
        session.next()
    elif sender == "DELETE":
        session.handle(eventDelete)
        session.next()
    elif sender == "IGNORE":
        session.next()
    elif sender == "MANUAL":
        dir_input = filedialog.askdirectory()
        if dir_input: 
            tmp = Pool(path=dir_input)
            session.handle(tmp)
            session.next()
    elif sender == "FINISH":
        session.finish()
    
    step = session.current_step()

    dpg.delete_item('raking')
    if step.is_running:
        CONTEXT.clear_pools_table()
        with dpg.child_window(parent='window', tag="raking", label="Raking"):
            with dpg.group(horizontal=True):
                with dpg.group(width=300):
                    with dpg.child_window(height=200, border=False):
                        if step.suggestions:
                            dpg.add_text('Suggested pools:')
                            for sgst in step.suggestions:
                                idx = CONTEXT.register_pool(sgst)
                                dpg.add_button(label=sgst.name, callback=update_raking, tag=f"POOL{idx}",
                                               width=-1)
                                dpg.bind_item_theme(dpg.last_item(), "theme_suggestion")
                                
                            dpg.add_separator()
                        else:
                            dpg.add_text("No pool suggestions")
                    with dpg.child_window(height=400, border=False):
                        for pool in CONTEXT.get_pools():
                            idx = CONTEXT.register_pool(pool)
                            dpg.add_button(label=pool.name, callback=update_raking, tag=f"POOL{idx}",
                                           width=-1)
                            dpg.bind_item_theme(dpg.last_item(), "theme_pool")
                    dpg.add_separator()
                    dpg.add_button(label='Ignore', callback=update_raking, tag=f"IGNORE",
                                   width=-1)
                    dpg.add_button(label='Choose location', callback=update_raking, tag=f"MANUAL",
                                   width=-1)
                    dpg.add_spacer(height=10)

                    dpg.add_button(label='Delete', callback=update_raking, tag=f"DELETE",
                                   width=-1)
                    dpg.bind_item_theme(dpg.last_item(), "theme_red")    
                    dpg.add_spacer(height=10)
                    dpg.add_button(label='Open file', tag="file-open",
                                   width=-1,
                                   callback=lambda : os.system(f'explorer "{step.file.resolve()}"'))
                    dpg.add_button(label='Reveal in explorer', tag="file-explore",
                                   width=-1,
                                   callback=lambda : subprocess.Popen(FILEOPENER + [step.file.resolve()]))
                    dpg.add_spacer(height=10)
                    dpg.add_button(label='Finish', tag="FINISH",
                                   width=-1,
                                   callback=update_raking)

                with dpg.child_window(height=-1): 
                    dpg.add_text(f'Reviewing {step.file.name}')
                    dpg.add_loading_indicator(tag="preview_loading")
                    with dpg.child_window(border=False):
                        preview_if_possible(step.file, CONTEXT)
                    dpg.delete_item("preview_loading")
    else:
        with dpg.child_window(parent='window', tag="raking", label="Raking"):
            dpg.add_text('All sorted!')
            if step.recycle_bin:
                dpg.add_text("You've marked following files for deletion:")
                for file in step.recycle_bin:
                    dpg.add_checkbox(label=file.name, tag=str(file),
                                    default_value=True)
                dpg.add_text("Are you sure you want to delete them?")
                dpg.add_text("Unmark the files you want to keep")

                def deletion_callback():
                    for file in step.recycle_bin:
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

with dpg.window(tag="window", label="main window"):
    with dpg.group(horizontal=True):
        dpg.add_button(label="Start raking", callback=start_raking, tag="start_raking")
        dpg.add_button(label="Change directory", callback=select_path)
        dpg.add_button(label="Settings", callback=lambda : open_settings_window(CONTEXT))
    dpg.add_text(f"Sorting path: {CONTEXT.get_path()}", tag='main label')
    

dpg.set_viewport_large_icon("assets/icon-big.ico")
dpg.set_viewport_small_icon("assets/icon.ico")

dpg.show_viewport()
dpg.set_primary_window("window", True)
dpg.start_dearpygui()
dpg.destroy_context()