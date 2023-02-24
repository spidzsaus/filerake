class Warning:
    def __init__(self, tip=None, **kwargs) -> None:
        if tip is None:
            tip = ''
        self.tip = tip
        for key, value in kwargs.items():
            self.__setattr__(key, value)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.tip}"


class FileExistsWarning(Warning):
    pass
