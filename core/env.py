from envdatareader import EnvDataReader
from typing import TypedDict


class database(TypedDict):
    host: str
    port: int
    user: str
    passwd: str
    dbName: str


env = EnvDataReader()

# основные чуствительные элементы
DB_CONNECT: database = {
    "host": env.get_value("DB_HOST", "localhost"),
    "port": int(env.get_value("DB_PORT", 5432)),
    "user": env.get_value("DB_USER", "postgres"),
    "passwd": env.get_value("DB_PASSWD"),
    "dbName": env.get_value("DB_NAME", "postgres")
}
