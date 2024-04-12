import psycopg2
import bcrypt
from core.env import DB_CONNECT
import json

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


async def logins(username: str, password: str):
    try:
        # Выполняем запрос
        cursor.execute("SELECT * FROM users WHERE login = %s", (username,))

        # Получаем пользователя по логину
        user = cursor.fetchone()

        # Проверяем, существует ли пользователь
        if not user:
            return False

        # Извлекаем данные о пользователе
        id, surname, name, login, passwords, role = user

        # Проверяем пароль
        if not verify_password(password, passwords):
            return False

        # Возвращаем данные пользователя
        return {
            "id": id,
            "role": role
        }

    except Exception as e:
        print("Ошибка при выполнении запроса:", e)


async def getUser(id: int) -> dict:
    try:
        cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
        res = cursor.fetchone()

        id, surname, name, login, passwords, role = res

        arra: dict = {
            "id": id,
            "surname": surname,
            "name": name,
            "role": role
        }

        return arra

    except Exception as e:
        pass


async def selectPropetry():
    try:
        cursor.execute("SELECT * FROM equipment ORDER BY unitid")
        res = cursor.fetchall()

        return res

    except Exception as e:
        pass


async def deletePropetry(id: int):
    try:
        cursor.execute("DELETE FROM equipment WHERE unitid = %s", (id,))
        engien.commit()
        return True
    except Exception as e:
        return False


async def editPropetry(unitname, datestart, cost, costyear, costafter, period, hallid, unitid):
    try:
        cursor.execute("UPDATE equipment SET unitname = %s, datestart = %s, cost = %s, costyear = %s, costafter = %s, period = %s, hallid = %s WHERE unitid = %s",
                       (unitname, datestart, cost, costyear, costafter, period, hallid, unitid))
        cursor.commmit()
    except Exception as e:
        pass


async def getPropetry(id):
    try:
        cursor.execute("SELECT * FROM equipment WHERE unitid = %s", (id,))
        res = cursor.fetchone()

        return res
    except Exception as e:
        pass


async def createPropetry(unitname, datestart, cost, costyear, costafter, period, hallid):
    try:
        cursor.execute("INSERT INTO equipment (unitname, datestart, cost, costyear, costafter, period, hallid) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (unitname, datestart, cost, costyear, costafter, period, hallid))
        engien.commit()
        return True
    except Exception as e:
        return False


async def selectBuilding():
    try:
        cursor.execute("SELECT * FROM buildings ORDER BY id_building")
        res = cursor.fetchall()
        return res
    except Exception as e:
        pass


async def getBuildingKadastr(id):
    try:
        cursor.execute("SELECT * FROM kadastr WHERE kadastr = %s", (id,))
        res = cursor.fetchone()
        return res
    except Exception as e:
        pass
    except psycopg2.errors.ForeignKeyViolation as e:
        engien.rollback()


async def getOneBuilding(id):
    try:
        cursor.execute("SELECT * FROM buildings WHERE id_building = %s", (id,))
        res = cursor.fetchone()
        return res
    except Exception as e:
        pass
    except psycopg2.errors.ForeignKeyViolation as e:
        engien.rollback()


async def createBuilding(buildingname, land, material, wear, flow, comment, id_kadastr):
    try:
        cursor.execute("INSERT INTO buildings (buildingname, land, material, wear, flow, comment, id_kadastr) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (buildingname, int(land), material, int(wear), int(flow), comment, int(id_kadastr)))
        engien.commit()
    except Exception as e:
        pass
    except psycopg2.errors.ForeignKeyViolation as e:
        engien.rollback()


async def deleteBuilding(id):
    try:
        cursor.execute("DELETE FROM buildings WHERE id_building = %s", (id,))
        engien.commit()
        return True
    except Exception as e:
        return False
    except psycopg2.errors.ForeignKeyViolation as e:
        engien.rollback()


async def editBuildingst(id, buildingname, land, material, wear, flow, comment, id_kadastr):
    try:
        cursor.execute("UPDATE buildings SET buildingname = %s, land = %s, material = %s, wear = %s, flow = %s, comment = %s, id_kadastr = %s WHERE id_building = %s",
                       (buildingname, int(land), material, int(wear), int(flow), comment, int(id_kadastr), id))
        engien.commit()
    except Exception as e:
        pass
    except psycopg2.errors.ForeignKeyViolation as e:
        engien.rollback()


async def selectKadastr():
    try:
        cursor.execute("SELECT * FROM kadastr ORDER BY kadastr")
        res = cursor.fetchall()
        return res
    except Exception as e:
        pass
    except psycopg2.errors.ForeignKeyViolation as e:
        engien.rollback()


async def getOneKadastr(id):
    try:
        cursor.execute("SELECT * FROM kadastr WHERE kadastr = %s", (id,))
        res = cursor.fetchone()
        return res
    except Exception as e:
        pass
    except psycopg2.errors.ForeignKeyViolation as e:
        engien.rollback()


async def editKadastrsOne(id, street, house, year):
    try:
        cursor.execute("UPDATE kadastr SET street = %s, house = %s, year = %s WHERE kadastr = %s",
                       (street, house, year, id))
        engien.commit()
    except Exception as e:
        pass
    except psycopg2.errors.ForeignKeyViolation as e:
        engien.rollback()


async def deleteKadastrs(id):
    try:
        cursor.execute("DELETE FROM kadastr WHERE kadastr = %s", (id,))
        engien.commit()
        return True
    except psycopg2.errors.ForeignKeyViolation as e:
        engien.rollback()
        return False
    except psycopg2.Error as e:
        pass
    except Exception as e:
        pass

async def createKadastrs(id, street, house, year):
    try:
        cursor.execute("INSERT INTO kadastr (kadastr, street, house, year) VALUES (%s, %s, %s, %s)",
                       (id, street, house, year))
        engien.commit()
    except Exception as e:
        pass
    except psycopg2.errors.ForeignKeyViolation as e:
        engien.rollback()
        return False