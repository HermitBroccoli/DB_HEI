from dotenv import load_dotenv
from typing import TypedDict
import os

load_dotenv('.env')

class database(TypedDict):
    host: str
    port: int
    user: str
    passwd: str
    dbName: str

# основные чуствительные элементы
DB_CONNECT: database = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "passwd": os.getenv("DB_PASSWD"),
    "dbName": os.getenv("DB_NAME")
}

print(DB_CONNECT)
