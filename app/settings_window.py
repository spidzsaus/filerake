import dearpygui.dearpygui as dpg

def open_settings_window(context):
    def apply_settings():
        context.__settings__.file_preview_text_line_limit = dpg.get_value("file_preview_text_line_limit")
        
        context.__settings__.write()
        dpg.delete_item("settings_window")


    with dpg.window(label="Settings", tag="settings_window"):
        with dpg.tree_node(label="File preview settings"):
            dpg.add_text("Text files preview line limit")
            dpg.add_input_int(default_value=context.__settings__.file_preview_text_line_limit, 
                              tag="file_preview_text_line_limit")
            dpg.add_spacing()
            dpg.add_text("Text file extensions")
            dpg.add_listbox(items=context.__settings__.text_formats,
                            tag="text_formats")
        dpg.add_separator()
        dpg.add_button(label="Apply", callback=apply_settings)

