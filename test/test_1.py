import pytest
import httpx

BASE_URL = "http://prod-team-12-ecl1h2gh.hack.prodcontest.ru:443"

# Тест регистрации студента
def test_register_student():
    payload = {
        "name": "Тест",
        "lastname": "Тестов",
        "patronim": "Тестович",
        "birthdate": "2005-09-01",
        "course": 2,
        "password": "testpassword",
        "gender": "Мужской",
        "hobby": "Шахматы",
        "bedtime": "22:00",
        "waketime": "07:00",
        "language": "Русский",
        "login": "testuser123"
    }
    with httpx.Client() as client:
        response = client.post(f"{BASE_URL}/register/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"
        assert "id" in data

# Тест создания комнаты с правильным токеном
def test_create_room_success():
    payload = {
        "tags": ["Тишина", "Чтение"],
        "sleep_time": "23:00",
        "capacity": 3,
        "admin_token": "SECRET_ADMIN_TOKEN"
    }
    with httpx.Client() as client:
        response = client.post(f"{BASE_URL}/create_room/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["status"] == "success"

# Тест получения списка всех комнат
def test_get_all_rooms():
    with httpx.Client() as client:
        response = client.get(f"{BASE_URL}/rooms/")
        assert response.status_code == 200
        data = response.json()
        assert "room_ids" in data
        assert isinstance(data["room_ids"], list)