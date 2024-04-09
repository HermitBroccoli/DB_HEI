import psycopg2
import bcrypt
from core.env import DB_CONNECT

from typing import TypedDict


class database(TypedDict):
    host: str
    port: int
    user: str
    passwd: str
    dbName: str


engien = psycopg2.connect(
    dbname=DB_CONNECT.get("dbName"),
    user=DB_CONNECT.get("user"),
    password=DB_CONNECT.get("passwd"),
    host=DB_CONNECT.get("host"),
    port=DB_CONNECT.get("port")
)

cursor = engien.cursor()


def verify_password(password: str, hash_password: str) -> bool:
    if not password:
        return False
    
    return bcrypt.checkpw(password.encode('utf-8'), hash_password.encode('utf-8'))

def login(username: str, password: str) -> None:
    try:
        cursor.execute("SELECT * FROM users WHERE login = %s", (username,))  # noqa

        user = cursor.fetchone()  # Получение первой строки результата запроса

        id, surname, name, login, passwords, role = user

        if not user:
            print("Неверный логин.")

        if not verify_password(password, passwords):
            return False

        return True

        

    except Exception as e:
        print("Ошибка при выполнении запроса:", e)


