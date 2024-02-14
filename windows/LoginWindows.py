from tkinter import Label, Frame, Entry, Button, ttk, messagebox
from database.connection import login
from features.hashing import PasswordManager
from windows import MainWindow, LayoutWindow


class LoginWindow(LayoutWindow):

    def __init__(self):
        super().__init__()
        self.title("Login")

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
        self.input1.focus_set()

        self.label2 = Label(self.frame, text="Пароль:", bg="black", fg="white")
        self.label2.grid(row=1, column=0, sticky="e")

        self.input2 = Entry(self.frame, show="*")
        self.input2.grid(row=1, column=1, padx=5, pady=5)

        self.button = Button(self.frame, text="Войти", command=self.__login)
        self.button.grid(row=2, columnspan=2)

    def __login(self):
        user = "".join(self.input1.get().split())
        password = self.input2.get()  # noqa

        login_res = login(username=user, func=self.__error_message)

        if not login_res:
            self.__error_message()
            return

        if not PasswordManager.verify_password(password, login_res.get("password")):  # noqa
            self.__error_message()
            return

        self.__main_open()

    def __error_message(self):
        messagebox.showerror("Ошибка", "Ошибка авторизации!")

    def __main_open(self):
        self.destroy()
        main_win = MainWindow("Университет")
        main_win.focus_force()
        main_win.mainloop()
