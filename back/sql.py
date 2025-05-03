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
            name TEXT NOT NULL,
            description TEXT DEFAULT 'Just common room',
            villagers_gender TEXT DEFAULT 'None',
            villagers_course TEXT DEFAULT 'None',
            capacity INTEGER DEFAULT 1,  # Вместимость (число)
            CHECK (capacity > 0)  # Вместимость не может быть нулём или отрицательной
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

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS RoomVillagers(
            room_id INTEGER,
            1st_villager_id INTEGER,
            PRIMARY KEY (room_id, villager_id),
            FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
        )
    ''')

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


def stud_login(login,password):
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT 1 FROM users WHERE username = ? AND password = ?",
            (login, password)
        )
        return cursor.fetchone() is not None




# Действия на учениками
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


def get_filtered(parametr, value):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    query = f"SELECT first_name, last_name, patronymic FROM Pupils_hobby WHERE {parametr} = ?"
    cursor.execute(query, (value,))
    result = cursor.fetchall()

    connection.close()
    return result




# Действия над комнатами
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


def all_rooms():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT room_id FROM Rooms')
    result = cursor.fetchall()

    connection.close()
    return result


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


def live_in_room(room_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute('SELECT villagers FROM Rooms WHERE room_id = ?', (room_id,))
    result = cursor.fetchall()

    connection.close()
    return result


def add_villager_to_room(room_id, villager_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # 1. Узнаём текущее количество жителей в комнате
    cursor.execute('''
        SELECT COUNT(*) FROM RoomVillagers 
        WHERE room_id = ?
    ''', (room_id,))
    current_count = cursor.fetchone()[0]

    # 2. Узнаём вместимость комнаты
    cursor.execute('''
        SELECT capacity FROM Rooms 
        WHERE room_id = ?
    ''', (room_id,))
    capacity = cursor.fetchone()[0]

    # 3. Проверяем, есть ли ещё место
    if current_count < capacity:
        cursor.execute('''
                INSERT INTO RoomVillagers (room_id, villager_id)
                VALUES (?, ?)
            ''', (room_id, villager_id))
        print(f"Житель {villager_id} добавлен в комнату {room_id}")
        return True
    else:
        return False

def get_villagers_in_room(room_id):
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    cursor.execute("""
        SELECT villager_id 
        FROM RoomVillagers 
        WHERE room_id = ?
        ORDER BY villager_id
    """, (room_id,))
    return [row[0] for row in cursor.fetchall()]  # Возвращает список ID жителей



# Инициализация базы при запуске
init_db()