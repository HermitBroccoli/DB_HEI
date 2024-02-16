from tkinter import Frame, Label


class ProfilePage(Frame):

    def __init__(self):
        super().__init__()

        self.label = Label(self, text="text")
        self.label.grid(row=0, column=0)
