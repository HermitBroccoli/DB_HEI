from tkinter import Tk


class LayoutWindow(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap("./icon/favicon.ico")
        self.resizable(False, False)
        self.geometry("1280x720")
