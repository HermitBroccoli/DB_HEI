import psycopg2 as db
from core.env import DB_CONNECT

engien = db.connect(
    dbname=DB_CONNECT.get("dbName"),
    user=DB_CONNECT.get("user"),
    password=DB_CONNECT.get("passwd"),
    host=DB_CONNECT.get("host"),
    port=DB_CONNECT.get("port")
)

cur = engien.cursor()

""" create database """

cur.execute(
    """CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            surname VARCHAR(50) NOT NULL,
            name VARCHAR(50) NOT NULL,
            login VARCHAR(50) NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL DEFAULT 'Преподаватель'
        )"""
)

cur.commit()

cur.execute("""
            CREATE TABLE IF NOT EXISTS Kadastr (
                kadastr INT PRIMARY KEY,
                street VARCHAR(100),
                house INT,
                year INT
);
""")

cur.commit()

cur.execute("""
    CREATE TABLE IF NOT EXISTS Buildings (
            id_building SERIAL PRIMARY KEY,
            id_kadastr INT REFERENCES Kadastr(kadastr),
            buildingName VARCHAR(100),
            land INT,
            material VARCHAR(50),
            wear INT,
            flow INT,
            comment TEXT
    );
            
""")

cur.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS Chiefs (
    chiefID INT PRIMARY KEY,
    lastName VARCHAR(100),
    firstName VARCHAR(100),
    patronymic VARCHAR(100),
    street VARCHAR(100),
    house INT,
    experience INT
);
""")
cur.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS BuildingPhotos (
    id_photo SERIAL PRIMARY KEY,
    id_building INT REFERENCES Buildings(id_building),
    photo BYTEA
);
""")
# -- В данном случае предполагается, что фотографии будут храниться в бинарном формате

cur.commit()

cur.execute("""
    CREATE TABLE IF NOT EXISTS Halls (
        hallID SERIAL PRIMARY KEY,
        square INT,
        windows INT,
        heating INT,
        target VARCHAR(100),
        buildingID INT REFERENCES Buildings(id_building),
        departmentID INT REFERENCES Departments(departmentID),
        materialResponsibleID INT REFERENCES Chiefs(chiefID)
    );
""")

cur.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS Equipment (
    unitID SERIAL PRIMARY KEY,
    unitName VARCHAR(100),
    dateStart DATE,
    cost NUMERIC(10, 2),
    costYear INT,
    costAfter NUMERIC(10, 2),
    period INT,
    hallID INT REFERENCES Halls(HallID)
);
""")

cur.commit()

cur.execute("""
CREATE TABLE IF NOT EXISTS Departments (
    departmentID SERIAL PRIMARY KEY,
    departmentName VARCHAR(100),
    boss VARCHAR(100),
    phone VARCHAR(20),
    officeDean VARCHAR(100)
)
""")


""" end create database """
