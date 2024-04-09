from tkinter import END, Tk, Label, Frame, Entry, Button, ttk
from database.connection import login
from tkinter.messagebox import showerror


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

        self.button = Button(self.frame, text="Войти", command=self.__login)
        self.button.grid(row=2, columnspan=2)

        self.input1.focus_set()

    def __login(self):
        logins = login(self.input1.get(), self.input2.get())

        if not logins:
            self.input1.delete(0, END)
            self.input2.delete(0, END)
            showerror(title="Ошибка", message="Неправильный логин или пароль")
            self.input1.focus_set()
            return

        self.destroy()
        from windows.MainWindows import MainWindow
        app = MainWindow()
        app.mainloop()

