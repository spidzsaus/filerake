import abc
import dearpygui.dearpygui as dpg


class BaseWindow(abc.ABC):
    tag: str
    window_kwargs: dict

    def __init__(self, **kwargs) -> None:
        self.window_kwargs = kwargs

    @abc.abstractmethod
    def draw(self):
        ...
    
    def render(self):
        dpg.delete_item(self.tag)
        with dpg.child_window(**self.window_kwargs):
            self.draw()
