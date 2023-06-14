import dearpygui.dearpygui as dpg

from app.windows.base_window import BaseWindow
from core.raking_session import Session

class SessionWindow(BaseWindow):
    session: Session

    def __init__(self, session: Session, **kwargs):
        self.session = session
        self.tag = 'session_window'
        self.current_file = session.next_file()
        super().__init__(**kwargs)
    
    def draw(self):
        with dpg.group(horizontal=True):
            with dpg.group(width=300):
                ...