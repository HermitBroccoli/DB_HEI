from tkinter import Menu
from tkinter.ttk import Notebook
from windows.LayoutWindows import LayoutWindow
from .tabs.ProfileFrame import ProfilePage


class MainWindow(LayoutWindow):

    def __init__(self, title: str):
        super().__init__()
        self.title(title)

        self.m = Menu(self)
        self.mf = Menu(self.m, tearoff=0)
        self.mf.add_separator()
        self.mf.add_command(label="Выход", command=self.destroy)

        self.m.add_cascade(label="Файл", menu=self.mf)

        self.tabs = Notebook(self)

        self.tabs.add(ProfilePage(), text="Профиль")

        self.tabs.pack(expand=1, fill="both")

        self.config(menu=self.m)
