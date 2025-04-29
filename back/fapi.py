from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from typing import List
import sqlite3

from back.sql import new_stud, new_room, room_info_by_id, stud_info_by_id, live_in_room, all_rooms

app = FastAPI(
    title="Dormitory Room Picker API",
    description="API для регистрации студентов, создания комнат и поиска лучших совпадений.",
    version="1.0.0",
    contact={
        "name": "команда 12"
    }
)


def create_tables():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Pupils_hobby (
            Stud_id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            patronymic TEXT,
            password TEXT NOT NULL,
            birthday_date DATE NOT NULL,
            course INTEGER NOT NULL,
            gender TEXT NOT NULL,
            hobby TEXT,
            bedtime TEXT,
            wakeup_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

create_tables()

# Модели
class StudentCreate(BaseModel):
    name: str = Field(..., example="Иван")
    lastname: str = Field(..., example="Иванов")
    patronim: str = Field(..., example="Иванович")
    birthdate: str = Field(..., example="2005-09-01")
    course: int = Field(..., example=2)
    password: str = Field(..., example="securepassword123")
    gender: str = Field(..., example="Мужской")
    hobby: str = Field(..., example="Гитара")
    bedtime: str = Field(..., example="23:00")
    waketime: str = Field(..., example="07:00")
    language: str = Field(..., example="Русский")
    login: str = Field(..., example="student123")

class RoomCreate(BaseModel):
    tags: List[str] = Field(..., example=["Тишина", "Чтение"])
    sleep_time: str = Field(..., example="23:00")
    capacity: int = Field(..., example=3)
    admin_token: str = Field(..., example="SECRET_ADMIN_TOKEN")


class RoomResponse(BaseModel):
    id: int
    tags: List[str]
    sleep_time: str
    capacity: int
    occupants: List[int]

# Эндпоинты
@app.post("/register/", status_code=status.HTTP_201_CREATED, summary="Регистрация студента", description="Создаёт нового студента и добавляет его в базу данных.")
async def create_student(student: StudentCreate):
    try:
        student_id = new_stud(
            name=student.name,
            lastname=student.lastname,
            patronymic=student.patronim,
            birthdate=student.birthdate,
            course=student.course,
            password=student.password,
            gender=student.gender,
            hobby=student.hobby,
            bedtime=student.bedtime,
            waketime=student.waketime,
            language=student.language,
            login=student.login
        )
        return {
            "id": student_id,
            "status": "success",
            "message": "Студент успешно зарегистрирован"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": f"Ошибка: {str(e)}"
            }
        )


@app.post("/create_room/", status_code=status.HTTP_201_CREATED, summary="Создание новой комнаты",
          description="Создаёт новую комнату в общежитии.")
async def create_room(room: RoomCreate):
    try:
        if room.admin_token != "SECRET_ADMIN_TOKEN":
            raise HTTPException(status_code=403, detail="Неверный токен администратора.")

        new_room(
            room_name="Комната с тэгами " + ", ".join(room.tags),
            room_description="Описание комнаты",
            rooms_villager_gender="Любой",
            room_villager_course="Любой",
            room_villagers="",
            capacity=room.capacity
        )
        return {
            "status": "success",
            "message": "Комната успешно создана."
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"status": "error", "message": f"Ошибка: {str(e)}"}
        )


@app.get("/rooms/", summary="Получение списка всех комнат", description="Возвращает список ID всех комнат.")
async def get_all_rooms():
    try:
        rooms = all_rooms()
        room_ids = [room[0] for room in rooms]
        return {"room_ids": room_ids}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/room/{room_id}", summary="Информация о комнате", description="Возвращает подробную информацию о комнате по её ID.")
async def get_room_info(room_id: int):
    try:
        info = room_info_by_id(room_id)
        if not info:
            raise HTTPException(status_code=404, detail="Комната не найдена")
        name, description, villagers_gender, villagers_course, villagers, capacity = info[0]
        return {
            "room_id": room_id,
            "name": name,
            "description": description,
            "villagers_gender": villagers_gender,
            "villagers_course": villagers_course,
            "villagers": villagers,
            "capacity": capacity
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/student/{stud_id}", summary="Информация о студенте", description="Возвращает подробную информацию о студенте по его ID.")
async def get_student_info(stud_id: int):
    try:
        info = stud_info_by_id(stud_id)
        if not info:
            raise HTTPException(status_code=404, detail="Студент не найден")
        (first_name, last_name, patronymic, login, password, birthday_date, course, gender, hobby, bedtime, wakeup_time) = info[0]
        return {
            "stud_id": stud_id,
            "first_name": first_name,
            "last_name": last_name,
            "patronymic": patronymic,
            "login": login,
            "birthday_date": birthday_date,
            "course": course,
            "gender": gender,
            "hobby": hobby,
            "bedtime": bedtime,
            "wakeup_time": wakeup_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Модель для входящих данных
class LoginData(BaseModel):
    login: str
    password: str

# Твоя функция проверки
def stud_login(login, password):
    with sqlite3.connect('database.db') as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT 1 FROM users WHERE username = ? AND password = ?",
            (login, password)
        )
        return cursor.fetchone() is not None

# Эндпоинт для логина
@app.post("/login")
def login(data: LoginData):
    if stud_login(data.login, data.password):
        return {"status": "success", "message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid login or password")
