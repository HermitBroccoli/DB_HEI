from tkinter import * # noqa
from tkinter import Tk


class MainWindow(Tk):

    def __init__(self, title: str):
        super().__init__()
        self.title = title
        self.geometry("1280x720")

        self.label = Label(
            self,
            text="Test"
        )

        self.label.grid(
            row=0,
            column=0
        )


def main():

    app = MainWindow("Университет")

    app.mainloop()


if __name__ == '__main__':
    main()
