import dearpygui.dearpygui as dpg
from tkinter import filedialog
import re
from pathlib import Path

from core.pools import Pool

def open_settings_window(context):
    dpg.delete_item("settings_window")

    settings = context.get_settings()

    local_pools = settings.pools[:]

    def apply_settings():
        settings.file_preview_text_line_limit = int(dpg.get_value("file_preview_text_line_limit"))
        update_local_pool_data()
        settings.pools = local_pools[:]
        settings.write()
        context.update_settings()
        dpg.delete_item("settings_window")

    def update_local_pool_data():
        for i, lp in enumerate(local_pools):
            name = dpg.get_value(f"POOL_NAME:{i}")
            pattern = dpg.get_value(f"POOL_PATTERN:{i}")
            path = dpg.get_value(f"POOL_PATH:{i}")
            if name is None or pattern is None or path is None:
                continue
            lp.name = name
            lp.pattern = re.compile(pattern)
            lp.path = Path(path)

    def add_new_pool_callback():
        new = Pool()
        new.name = "New pool"
        new.pattern = re.compile("")
        new.path = Path("C:/")
        local_pools.append(new)
        update_local_pool_data()
        redraw_pools_menu(True)
    
    def delete_pool_callback(sender):
        idx = int(sender.lstrip('POOL_DELETE:'))
        pool = local_pools[idx]
        def delete_sure():
            update_local_pool_data()
            local_pools.pop(idx)
            dpg.delete_item("are_you_sure_pool")
            redraw_pools_menu(True)

        dpg.delete_item("are_you_sure_pool")
        with dpg.window(label="Delete pool", tag="are_you_sure_pool"):
            dpg.add_text(f"Are you sure you want to delete pool {pool.name}?")
            with dpg.group(horizontal=True):
                dpg.add_button(label="Delete pool", callback=delete_sure)
                dpg.add_button(label="Cancel", callback=lambda :  dpg.delete_item("are_you_sure_pool"))
        

    def redraw_pools_menu(opened=False):
        dpg.delete_item("settings_pools_list")
        with dpg.tree_node(default_open=opened, parent="settings_pools_menu", label="Pools", tag="settings_pools_list"):
            for i, pool in enumerate(local_pools):
                dpg.add_text("Name")
                dpg.add_input_text(default_value=pool.name, tag=f"POOL_NAME:{i}")
                dpg.add_text("Regex suggestion pattern")
                dpg.add_input_text(default_value=pool.pattern.pattern, tag=f"POOL_PATTERN:{i}")
                dpg.add_text("Path")
                def change_path():
                    dir_input = filedialog.askdirectory()
                    if not dir_input: return
                    dpg.set_value(f"POOL_PATH:{i}", dir_input)

                with dpg.group(horizontal=True):
                    dpg.add_input_text(default_value=str(pool.path), tag=f"POOL_PATH:{i}")
                    dpg.add_button(label="Select directory", callback=change_path)
                dpg.add_button(label="Delete", callback=delete_pool_callback, tag=f"POOL_DELETE:{i}")
                dpg.add_spacer(height=10)
            dpg.add_separator()
            dpg.add_button(label="Add new pool", callback=add_new_pool_callback)


    with dpg.window(label="Settings", tag="settings_window"):
        with dpg.tree_node(label="File preview settings"):
            dpg.add_text("Text files preview line limit")
            dpg.add_input_int(default_value=settings.file_preview_text_line_limit, 
                              tag="file_preview_text_line_limit")
            dpg.add_spacer(height=10)
            dpg.add_text("Text file extensions")
            dpg.add_listbox(items=settings.text_formats,
                            tag="text_formats")
        dpg.add_separator()
        with dpg.group(tag="settings_pools_menu"):
            redraw_pools_menu()

        dpg.add_separator()
        dpg.add_button(label="Apply", callback=apply_settings)

