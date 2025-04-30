import sqlite3
import random

# Инициализация базы данных (создание таблиц)
def init_db():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Таблица отзывов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            stud_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
            comment TEXT,
            photo_filename TEXT
        )
    ''')

    # Таблица комнат
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Rooms(
            room_id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT DEFAULT 'Just common room',
            villagers_gender TEXT DEFAULT 'None',
            villagers_course TEXT DEFAULT 'None',
            villagers TEXT DEFAULT 'Anybody',
            capacity TEXT DEFAULT 'Anybody'
        )
    ''')

    # Таблица учеников + увлечения
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pupils_hobby(
            stud_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            patronymic TEXT DEFAULT 'Unknown',
            login TEXT,
            password TEXT,
            birthday_date TEXT,
            course INTEGER,
            gender TEXT,
            language TEXT,
            hobby TEXT DEFAULT 'Unknown',
            bedtime TEXT,
            wakeup_time TEXT
        )
    ''')

    connection.commit()
    connection.close()

# Функция для добавления нового студента
def new_stud(name, lastname, patronymic, login, password, birthdate, course, gender, language, hobby, bedtime, waketime):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    stud_id = random.randint(100000, 999999)
    cursor.execute('''
        INSERT INTO Pupils_hobby(stud_id, first_name, last_name, login, patronymic, password, birthday_date, course, gender, language, hobby, bedtime, wakeup_time)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (stud_id, name, lastname, patronymic, login, password, birthdate, course, gender, language, hobby, bedtime, waketime))

    connection.commit()
    connection.close()
    return stud_id

# Функция для добавления новой комнаты
def new_room(room_name, room_description, rooms_villager_gender, room_villager_course, room_villagers, capacity):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    room_id = random.randint(100000, 999999)
    cursor.execute('''
        INSERT INTO Rooms(room_id, name, description, villagers_gender, villagers_course, villagers, capacity)
        VALUES(?, ?, ?, ?, ?, ?, ?)
    ''', (room_id, room_name, room_description, rooms_villager_gender, room_villager_course, room_villagers, capacity))

    connection.commit()
    connection.close()

# Функция для добавления нового отзыва
def new_response(room_id, stud_id, rating, comment, photo_filename):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    review_id = random.randint(10000000, 99999999)
    cursor.execute('''
        INSERT INTO reviews(id, room_id, stud_id, rating, comment, photo_filename)
        VALUES(?, ?, ?, ?, ?, ?)
    ''', (review_id, room_id, stud_id, rating, comment, photo_filename))

    connection.commit()
    connection.close()

# Получить все комнаты
def all_rooms():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT room_id FROM Rooms')
    result = cursor.fetchall()

    connection.close()
    return result

# Получить информацию о комнате по id
def room_info_by_id(room_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''
        SELECT name, description, villagers_gender, villagers_course, villagers, capacity
        FROM Rooms WHERE room_id = ?
    ''', (room_id,))
    result = cursor.fetchall()

    connection.close()
    return result

# Получить информацию о студенте по id
def stud_info_by_id(stud_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('''
        SELECT first_name, last_name, patronymic, password, birthday_date, course, gender, language, hobby, bedtime, wakeup_time
        FROM Pupils_hobby WHERE stud_id = ?
    ''', (stud_id,))
    result = cursor.fetchall()

    connection.close()
    return result

# Кто живёт в комнате
def live_in_room(room_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT villagers FROM Rooms WHERE room_id = ?', (room_id,))
    result = cursor.fetchall()

    connection.close()
    return result

# Поиск учеников по какому-то параметру
def get_filtered_stud(parametr, value):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    avaible_rooms = []

    cursor.execute(f"SELECT id FROM Pupils_hobby WHERE {parametr} = ?", (value,))
    result = cursor.fetchall()
    for i in range(len(result)):
        one_res = result[i]
        cursor.execute('SELECT room_id, name FROM Rooms WHERE villagers = ?',(one_res))
        avaible_rooms.append(cursor.fetchall())

    print(avaible_rooms)
    connection.close()
    return result


def get_filtered_room(parametr, value):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute(f"SELECT id, first_name, last_name, patronymic FROM Pupils_hobby WHERE {parametr} = ?", (value,))
    result = cursor.fetchall()
    for i in range(len(result)):
        one_res = result[i]


    connection.close()

    return result

def stud_login(login,password):
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT 1 FROM users WHERE username = ? AND password = ?",
            (login, password)
        )
        return cursor.fetchone() is not None

# Инициализация базы при запуске
init_db()