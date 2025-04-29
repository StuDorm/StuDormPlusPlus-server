import requests
import json
from datetime import datetime

# Конфигурация
BASE_URL = "http://localhost:443"  # URL вашего сервера
ENDPOINT = "/register/"

# Тестовые данные
test_student = {
    "name": "Иван",
    "lastname": "Иванов",
    "patronim": "Иванович",
    "birthdate": "2000-01-01",
    "course": 3,
    "password": "secret123",
    "gender": "мужской",
    "hobby": "плавание",
    "bedtime": "23:00",
    "waketime": "07:30"
}


def test_registration():
    url = f"{BASE_URL}{ENDPOINT}"

    try:
        # Отправляем POST-запрос
        response = requests.post(url, json=test_student)

        # Проверяем статус код
        assert response.status_code == 201, f"Ожидался статус 201, получен {response.status_code}"

        # Парсим ответ
        response_data = response.json()

        # Проверяем структуру ответа
        assert "id" in response_data, "Ответ не содержит ID студента"
        assert response_data["status"] == "success", "Статус не 'success'"

        print("Тест пройден успешно!")
        print("Ответ сервера:")
        print(json.dumps(response_data, indent=2, ensure_ascii=False))

        return True

    except Exception as e:
        print(f"Тест провален: {str(e)}")
        if 'response' in locals():
            print(f"Статус код: {response.status_code}")
            print(f"Ответ сервера: {response.text}")
        return False


print("Запуск теста регистрации студента...")
print(f"Время начала: {datetime.now().strftime('%H:%M:%S')}")
print("=" * 50)

success = test_registration()

print("=" * 50)
print(f"Результат теста: {'УСПЕХ' if success else 'ПРОВАЛ'}")