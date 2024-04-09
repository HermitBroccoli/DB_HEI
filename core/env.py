from dotenv import load_dotenv
from envdatareader import EnvDataReader
from typing import TypedDict
import os

env = EnvDataReader()

class database(TypedDict):
    host: str
    port: int
    user: str
    passwd: str
    dbName: str

# основные чуствительные элементы
DB_CONNECT: database = {
    "host": env.get_value("DB_HOST"),
    "port": env.get_value("DB_PORT"),
    "user": env.get_value("DB_USER"),
    "passwd": env.get_value("DB_PASSWD"),
    "dbName": env.get_value("DB_NAME")
}

print(DB_CONNECT)
