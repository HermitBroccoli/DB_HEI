from tkinter import Tk, Label, Frame, Entry, Button, ttk


class LoginWindow(Tk):

    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("1280x720")

        # Создаем стиль ttk (темный)
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure(bg="black")  # Задаем цвет фона всего окна
        self.style.configure("TLabel", background="black", foreground="white")
        self.style.configure("TButton", background="black", foreground="white")
        self.style.configure("TEntry",
                             fieldbackground="black",
                             foreground="white")

        self.frame = Frame(self, bg="black")
        self.frame.place(relx=0.5, rely=0.5, anchor="center")  # размещение фрейма по центру окна # noqa

        self.label1 = Label(self.frame, text="Логин:", bg="black", fg="white")
        self.label1.grid(row=0, column=0, sticky="e")

        self.input1 = Entry(self.frame)
        self.input1.grid(row=0, column=1, padx=5, pady=5)

        self.label2 = Label(self.frame, text="Пароль:", bg="black", fg="white")
        self.label2.grid(row=1, column=0, sticky="e")

        self.input2 = Entry(self.frame, show="*")
        self.input2.grid(row=1, column=1, padx=5, pady=5)

        self.button = Button(self.frame, text="Войти")
        self.button.grid(row=2, columnspan=2)

    def __login(self, username: str, password: str):
        pass