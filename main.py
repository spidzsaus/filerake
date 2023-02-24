from tkinter import filedialog
import dearpygui.dearpygui as dpg
from pathlib import Path

from app.settings import UserSettings
from app.raking_session import RakingSession, RakingStep

class Context:
    __searchPath__ = Path('C:/')
    __settings__ = UserSettings('config/settings.json')
    __session__ : RakingSession = None
    __tempPoolsTable__ = {}

def select_path(sender, app_data):
    dir_input = filedialog.askdirectory()
    if not dir_input: return
    Context.__searchPath__ = Path(dir_input)
    dpg.set_value('main label',
                  f"Sorting path: {Context.__searchPath__}")

def start_raking(sender, app_data):
    Context.__session__ = RakingSession(Context.__searchPath__, Context.__settings__)
    next_raking(..., ...)

def next_raking(sender, app_data):
    if sender is not Ellipsis:
        pool = Context.__tempPoolsTable__[int(sender[len('POOL'):])]
    else:
        pool = None
    step = Context.__session__.next(pool)
    dpg.delete_item('raking')
    if step:
        count = 0
        Context.__tempPoolsTable__.clear()
        with dpg.child_window(parent='window', tag="raking", label="Raking"):
            dpg.add_text(f'Reviewing {step.file.name}')

            if step.suggestions:
                dpg.add_text('Suggested pools:')
                for sgst in step.suggestions:
                    dpg.add_selectable(label=sgst.name, callback=next_raking, tag=f"POOL{count}")
                    Context.__tempPoolsTable__[count] = sgst
                    count += 1
                dpg.add_separator()
            for pool in step.pools:
                dpg.add_selectable(label=pool.name, callback=next_raking, tag=f"POOL{count}")
                Context.__tempPoolsTable__[count] = pool
                count += 1


dpg.create_context()
dpg.create_viewport(title="spidz.filerake")
dpg.setup_dearpygui()

with dpg.font_registry ():
    with dpg.font("assets\\fonts\\juliamono\\JuliaMono-Regular.ttf", 18, default_font=True, tag="cyr"):
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)

dpg.bind_font("cyr")

with dpg.window(tag="window", label="Example Window"):
    dpg.add_text(f"Sorting path: {Context.__searchPath__}", tag='main label')
    dpg.add_button(label="Change directory", callback=select_path)
    dpg.add_button(label="Start raking", callback=start_raking)


dpg.show_viewport()
dpg.set_primary_window("window", True)
dpg.start_dearpygui()
dpg.destroy_context()