from tkinter import Label, Menu
from windows.LayoutWindows import LayoutWindow


class MainWindow(LayoutWindow):

    def __init__(self, title: str):
        super().__init__()
        self.title(title)

        self.label = Label(self, text="Test")

        self.label.grid(row=0, column=0)

        m = Menu(self)
        mf = Menu(m, tearoff=0)
        mf.add_separator()
        mf.add_command(label="Exit", command=self.destroy)

        m.add_cascade(label="Файл", menu=mf)

        self.config(menu=m)
