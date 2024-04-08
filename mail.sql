CREATE EXTENSION pgcrypto;

CREATE TABLE
    IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        surname VARCHAR(50) NOT NULL,
        name VARCHAR(50) NOT NULL,
        login VARCHAR(50) NOT NULL,
        password VARCHAR(50) NOT NULL,
        role VARCHAR(50) NOT NULL DEFAULT 'Преподаваатель'
    );

CREATE TABLE
    IF NOT EXISTS kadastr (
        kadastr INT PRIMARY KEY,
        street VARCHAR(100),
        house INT,
        year INT
    );

CREATE TABLE
    IF NOT EXISTS buildings (
        id_building SERIAL PRIMARY KEY,
        id_kadastr INT REFERENCES Kadastr (kadastr),
        buildingName VARCHAR(100),
        land INT,
        material VARCHAR(50),
        wear INT,
        flow INT,
        comment TEXT
    );

CREATE TABLE
    IF NOT EXISTS chiefs (
        chiefID INT PRIMARY KEY,
        lastName VARCHAR(100),
        firstName VARCHAR(100),
        patronymic VARCHAR(100),
        street VARCHAR(100),
        house INT,
        experience INT
    );

CREATE TABLE
    IF NOT EXISTS buildingPhotos (
        id_photo SERIAL PRIMARY KEY,
        id_building INT REFERENCES Buildings (id_building),
        photo BYTEA
    );

CREATE TABLE
    IF NOT EXISTS halls (
        hallID SERIAL PRIMARY KEY,
        square INT,
        windows INT,
        heating INT,
        target VARCHAR(100),
        buildingID INT REFERENCES Buildings (id_building),
        departmentID INT REFERENCES Departments (departmentID),
        materialResponsibleID INT REFERENCES Chiefs (chiefID)
    );

CREATE TABLE
    IF NOT EXISTS equipment (
        unitID SERIAL PRIMARY KEY,
        unitName VARCHAR(100),
        dateStart DATE,
        cost NUMERIC(10, 2),
        costYear INT,
        costAfter NUMERIC(10, 2),
        period INT,
        hallID INT REFERENCES Halls (HallID)
    );

CREATE TABLE
    IF NOT EXISTS departments (
        departmentID SERIAL PRIMARY KEY,
        departmentName VARCHAR(100),
        boss VARCHAR(100),
        phone VARCHAR(20),
        officeDean VARCHAR(100)
    );

-- INSERT INTO
INSERT INTO users (surname, name, login, password, role) VALUES ('Кузьменко', 'Богдан', 'gbroccoli', crypt('qXmZZ7U8', gen_salt('md5')), 'Администратор');
INSERT INTO users (surname, name, login, password, role) VALUES ('Кузьменко', 'Богдан', 'gbroccoli', crypt('qXmZZ7U8', gen_salt('md5')), 'Преподаватель');
INSERT INTO users (surname, name, login, password, role) VALUES ('Кузьменко', 'Богдан', 'gbroccoli', crypt('qXmZZ7U8', gen_salt('md5')), '');
INSERT INTO users (surname, name, login, password, role) VALUES ('Кузьменко', 'Богдан', 'gbroccoli', crypt('qXmZZ7U8', gen_salt('md5')), 'Преподаватель');
INSERT INTO users (surname, name, login, password, role) VALUES ('Кузьменко', 'Богдан', 'gbroccoli', crypt('qXmZZ7U8', gen_salt('md5')), 'Преподаватель');
INSERT INTO users (surname, name, login, password, role) VALUES ('Кузьменко', 'Богдан', 'gbroccoli', crypt('qXmZZ7U8', gen_salt('md5')), 'Преподаватель');
INSERT INTO users (surname, name, login, password, role) VALUES ('Кузьменко', 'Богдан', 'gbroccoli', crypt('qXmZZ7U8', gen_salt('md5')), 'Преподаватель');
INSERT INTO users (surname, name, login, password, role) VALUES ('Кузьменко', 'Богдан', 'gbroccoli', crypt('qXmZZ7U8', gen_salt('md5')), 'Преподаватель');
INSERT INTO users (surname, name, login, password, role) VALUES ('Кузьменко', 'Богдан', 'gbroccoli', crypt('qXmZZ7U8', gen_salt('md5')), 'Преподаватель');
INSERT INTO users (surname, name, login, password, role) VALUES ('Кузьменко', 'Богдан', 'gbroccoli', crypt('qXmZZ7U8', gen_salt('md5')), 'Преподаватель');