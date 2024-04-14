/* 
PostgreSQL 16.1 (Debian 16.1-1.pgdg120+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
This is a database dump for the educational project (coursework) on the subject of Databases

version: v1.0

 */
 
CREATE EXTENSION pgcrypto;

CREATE TABLE
    IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        surname VARCHAR(50) NOT NULL,
        name VARCHAR(50) NOT NULL,
        login VARCHAR(50) NOT NULL,
        password VARCHAR(255) NOT NULL,
        role VARCHAR(50) NOT NULL DEFAULT 'Преподаваатель'
    );

CREATE TABLE
    IF NOT EXISTS departments (
        departmentID SERIAL PRIMARY KEY,
        departmentName VARCHAR(100),
        boss VARCHAR(100),
        phone VARCHAR(20),
        officeDean VARCHAR(100)
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
        id_kadastr INT REFERENCES kadastr (kadastr),
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
        patronymic VARCHAR(100) DEFAULT '',
        street VARCHAR(100),
        house INT,
        experience INT
    );

CREATE TABLE
    IF NOT EXISTS buildingPhotos (
        id_photo SERIAL PRIMARY KEY,
        id_building INT REFERENCES buildings (id_building),
        photo VARCHAR(255) NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS halls (
        hallID SERIAL PRIMARY KEY,
        square INT,
        windows INT,
        heating INT,
        target VARCHAR(100),
        buildingID INT REFERENCES buildings (id_building),
        departmentID INT REFERENCES departments (departmentID),
        materialResponsibleID INT REFERENCES chiefs (chiefID)
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
        hallID INT REFERENCES halls (HallID)
    );

-- INSERT INTO
INSERT INTO
    users (surname, name, login, password, role)
VALUES
    (
        'Кузьменко',
        'Богдан',
        'gbroccoli',
        '$2b$12$CjT.UzXaRq3/7hUOfOjDrOtfU2OqwrCzzdln0ry8A23cQ.dZgEEdK',
        'Администратор'
    );

-- Admin
INSERT INTO
    users (surname, name, login, password, role)
VALUES
    (
        'Смирнов',
        'Алексей',
        'alex_smirnov',
        '$2b$12$2HaMsFP4vqUnwJ2oL334DODQlzajmm4F3W/7SOMvzKkffO.jXkor.',
        'Преподаватель'
    );

INSERT INTO
    users (surname, name, login, password, role)
VALUES
    (
        'Попов',
        'Андрей',
        'andrey_popov',
        '$2b$12$rlH5HDu5ZCkyKrSWdrnYTeCqJo4tYEmta/xh7FzkNaHsKx93.IpDO',
        'Материально. отвественный'
    );

INSERT INTO
    users (surname, name, login, password, role)
VALUES
    (
        'Васильев',
        'Дмитрий',
        'dmitry_vasilyev',
        '$2b$12$AOniInn8qRkA/TcBF1kAvu/XuHM74yeu8aKs76VhcqL9V7b/1ONFe',
        'Преподаватель'
    );

INSERT INTO
    users (surname, name, login, password, role)
VALUES
    (
        'Петрова',
        'Елена',
        'elena_petrova',
        '$2b$12$siH/7SrHERtO4xEteWH2gO89klI8vSFNQEtTxH9ePkEc4ZfE9tf2y',
        'Преподаватель'
    );

INSERT INTO
    users (surname, name, login, password, role)
VALUES
    (
        'Соколов',
        'Игорь',
        'igor_sokolov',
        '$2b$12$J0pH3d5hnVsTiCd/ejDsSe6w5DihWnoVSBfUV2AaFQbUxi.p2dUPC',
        'Материально. отвественный'
    );

INSERT INTO
    users (surname, name, login, password, role)
VALUES
    (
        'Михайлов',
        'Олег',
        'oleg_mikhailov',
        '$2b$12$ZtaZtOur4y0qndyIQc5z/ODnn0xB6JBCXWrD.TcRZixQPSQs7OMH.',
        'Преподаватель'
    );

INSERT INTO
    users (surname, name, login, password, role)
VALUES
    (
        'Новиков',
        'Владимир',
        'vladimir_novikov',
        '$2b$12$5BqfIT1Db3Bvhp3LDrrCLeklf7uN6DyMBNN0VRmF/NklRXyQSrkPi',
        'Преподаватель'
    );

INSERT INTO
    users (surname, name, login, password, role)
VALUES
    (
        'Федоров',
        'Максим',
        'maxim_fedorov',
        '$2b$12$m9R9fzy7.92Gk4t.zT4fYuHxhyKd2dXVcaFXCkUBXPs8xddoDehtK',
        'Преподаватель'
    );

INSERT INTO
    users (surname, name, login, password, role)
VALUES
    (
        'Морозова',
        'Анастасия',
        'anastasia_morozova',
        '$2b$12$bamUiT1sDD3mBXhwC2pD6egBirQUHgTd6t1UdA2zIoa56QPkg50aG',
        'Материально. отвественный'
    );

INSERT INTO
    kadastr (kadastr, street, house, year)
VALUES
    (1001, 'Улица Ленина', 10, 2005),
    (1002, 'Улица Пушкина', 20, 2010),
    (1003, 'Улица Гагарина', 30, 2015),
    (1004, 'Улица Чехова', 40, 2020),
    (1005, 'Улица Толстого', 50, 2022),
    (1006, 'Улица Достоевского', 60, 2018),
    (1007, 'Улица Бродского', 70, 2017),
    (1008, 'Улица Маяковского', 80, 2019),
    (1009, 'Улица Есенина', 90, 2016),
    (1010, 'Улица Грибоедова', 100, 2014);

INSERT INTO
    buildings (
        id_kadastr,
        buildingName,
        land,
        material,
        wear,
        flow,
        comment
    )
VALUES
    (
        1001,
        'Дом №1',
        500,
        'Кирпич',
        10,
        3,
        'Нет особых комментариев'
    ),
    (
        1002,
        'Дом №2',
        700,
        'Панель',
        8,
        2,
        'Требуется ремонт крыши'
    ),
    (
        1003,
        'Дом №3',
        800,
        'Панель',
        15,
        1,
        'Недавно отремонтирован'
    ),
    (
        1004,
        'Дом №4',
        600,
        'Кирпич',
        20,
        4,
        'Требуется утепление стен'
    ),
    (
        1005,
        'Дом №5',
        1000,
        'Кирпич',
        12,
        2,
        'Все в хорошем состоянии'
    ),
    (
        1006,
        'Дом №6',
        900,
        'Панель',
        18,
        3,
        'Нет особых комментариев'
    ),
    (
        1007,
        'Дом №7',
        400,
        'Кирпич',
        25,
        5,
        'Требуется замена окон'
    ),
    (
        1008,
        'Дом №8',
        300,
        'Панель',
        30,
        4,
        'Нужно обновление сантехники'
    ),
    (
        1009,
        'Дом №9',
        1200,
        'Панель',
        22,
        3,
        'Требуется ремонт фасада'
    ),
    (
        1010,
        'Дом №10',
        1100,
        'Панель',
        17,
        2,
        'Недавно сделан капитальный ремонт'
    );

INSERT INTO
    chiefs (
        chiefID,
        lastName,
        firstName,
        patronymic,
        street,
        house,
        experience
    )
SELECT
    id,
    surname,
    name,
    '',
    -- Отчество, если есть (значение будет пустым)
    CONCAT ('Улица ', name),
    -- Вымышленная улица, сформированная на основе имени пользователя
    FLOOR(RANDOM () * 100) + 1,
    -- Вымышленный номер дома от 1 до 100
    FLOOR(RANDOM () * 20) + 1 -- Вымышленный опыт работы от 1 до 20 лет
FROM
    users
WHERE
    role = 'Материально. отвественный';

INSERT INTO
    buildingPhotos (id_building, photo)
VALUES
    (
        1,
        decode (
            'FFD8FFE000104A46494600010101004800480000FFE100684578696600004D4D002A00000008000601120003000000010000010100000001000002000000100000010000012A000500000001000000F6000003010200020000000F00010001000000310000000B00000001',
            'hex'
        )
    ),
    (
        2,
        decode (
            'FFD8FFE000104A46494600010101004800480000FFE100684578696600004D4D002A00000008000601120003000000010000010100000001000002000000100000010000012A000500000001000000F6000003010200020000000F00010001000000310000000B00000001',
            'hex'
        )
    ),
    (
        3,
        decode (
            'FFD8FFE000104A46494600010101004800480000FFE100684578696600004D4D002A00000008000601120003000000010000010100000001000002000000100000010000012A000500000001000000F6000003010200020000000F00010001000000310000000B00000001',
            'hex'
        )
    );

INSERT INTO
    departments (departmentName, boss, phone, officeDean)
VALUES
    (
        'Отдел компьютерных наук',
        'Иванов Петр Сергеевич',
        '+79991234567',
        'Смирнов Александр Иванович'
    ),
    (
        'Отдел физики',
        'Петров Андрей Васильевич',
        '+79181234567',
        'Козлова Елена Михайловна'
    ),
    (
        'Отдел химии',
        'Сидорова Мария Николаевна',
        '89001234567',
        'Иванова Ольга Алексеевна'
    ),
    (
        'Отдел биологии',
        'Козлов Игорь Петрович',
        '+79991234568',
        'Соколов Дмитрий Владимирович'
    ),
    (
        'Отдел математики',
        'Михайлова Наталья Ивановна',
        '89181234568',
        'Петров Павел Сергеевич'
    );

INSERT INTO
    halls (
        square,
        windows,
        heating,
        target,
        buildingID,
        departmentID,
        materialResponsibleID
    )
VALUES
    (120, 4, 1, 'Конференц-зал', 1, 1, 3),
    (80, 3, 1, 'Лекционный зал', 2, 2, 6),
    (150, 5, 1, 'Аудитория', 3, 3, 10),
    (90, 2, 0, 'Семинарская комната', 4, 4, 3),
    (100, 4, 1, 'Конференц-зал', 5, 5, 6),
    (130, 3, 1, 'Лекционный зал', 6, 1, 10),
    (140, 6, 1, 'Аудитория', 7, 2, 3),
    (110, 3, 0, 'Семинарская комната', 8, 3, 6),
    (160, 5, 1, 'Конференц-зал', 9, 4, 10),
    (70, 2, 1, 'Лекционный зал', 10, 5, 3);

INSERT INTO
    equipment (
        unitName,
        dateStart,
        cost,
        costYear,
        costAfter,
        period,
        hallID
    )
VALUES
    (
        'Проектор',
        '2023-01-15',
        1500.00,
        300,
        1000.00,
        5,
        1
    ),
    (
        'Компьютер',
        '2022-08-20',
        1200.00,
        250,
        800.00,
        4,
        2
    ),
    (
        'Микрофон',
        '2023-03-10',
        500.00,
        100,
        300.00,
        3,
        3
    ),
    (
        'Ноутбук',
        '2022-11-05',
        1800.00,
        350,
        1200.00,
        5,
        4
    ),
    (
        'Принтер',
        '2023-02-28',
        700.00,
        150,
        500.00,
        4,
        5
    ),
    ('Стол', '2022-10-12', 300.00, 50, 200.00, 3, 6),
    ('Стул', '2022-12-20', 100.00, 20, 70.00, 2, 7),
    (
        'Проектор',
        '2023-04-02',
        1500.00,
        300,
        1000.00,
        5,
        8
    ),
    (
        'Компьютер',
        '2022-09-15',
        1200.00,
        250,
        800.00,
        4,
        9
    ),
    (
        'Микрофон',
        '2023-05-10',
        500.00,
        100,
        300.00,
        3,
        10
    );