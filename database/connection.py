import psycopg2
from typing import Callable
from core.env import DB_CONNECT


engien = psycopg2.connect(
    dbname=DB_CONNECT.get("dbName"),
    user=DB_CONNECT.get("user"),
    password=DB_CONNECT.get("passwd"),
    host=DB_CONNECT.get("host"),
    port=DB_CONNECT.get("port")
)

cursor = engien.cursor()


def login(username: str, func: Callable[[], None]):
    try:
        cursor.execute("SELECT * FROM users WHERE login = %s", (username,))  # noqa

        user = cursor.fetchone()  # Получение первой строки результата запроса

        if not user:
            return

        id, login, password, role = user

        return {"id": id, "login": login, "password": password, "role": role}

    except Exception as e:
        print("Ошибка при выполнении запроса:", e)
