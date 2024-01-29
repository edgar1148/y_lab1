import pytest
from fastapi.testclient import TestClient
from app.main import app


# Создание тестового клиента
client = TestClient(app)

# Переменные окружения
target_menu_id = None
target_submenu_id = None
target_dish_id = None

def test_create_menu():
    # Отправка POST-запроса для создания меню
    response = client.post("/api/v1/menus/", json={"title": "My menu 1", "description": "My menu description 1"})
    # Проверка, что статус ответа - 201 CREATED
    assert response.status_code == 201
    # Сохранение id в переменной окружения
    global target_menu_id
    target_menu_id = response.json()["id"]

def test_create_submenu():
    # Отправка POST-запроса для создания подменю
    response = client.post(f"/api/v1/menus/{target_menu_id}/submenus/", json={"title": "My submenu 1", "description": "My submenu description 1"})
    # Проверка, что статус ответа - 201 CREATED
    assert response.status_code == 201
    # Сохранение id в переменной окружения
    global target_submenu_id
    target_submenu_id = response.json()["id"]

def test_create_dish():
    # Отправка POST-запроса для создания блюда
    response = client.post(f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/", json={"title": "My dish 2", "description": "My dish description 2", "price": "13.50"})
    # Проверка, что статус ответа - 201 CREATED
    assert response.status_code == 201
    # Сохранение id в переменной окружения
    global target_dish_id
    target_dish_id = response.json()["id"]

def test_create_second_dish():
    # Отправка POST-запроса для создания второго блюда
    response = client.post(f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/", json={"title": "My dish 1", "description": "My dish description 1", "price": "12.50"})
    # Проверка, что статус ответа - 201 CREATED
    assert response.status_code == 201
    # Сохранение id в переменной окружения
    global target_dish_id
    target_dish_id = response.json()["id"]

def test_get_menu():
    # Отправка GET-запроса для получения информации о меню
    response = client.get(f"/api/v1/menus/{target_menu_id}")
    # Проверка, что статус ответа - 200 OK
    assert response.status_code == 200
    # Получение данных из ответа
    response_data = response.json()
    # Проверка, что id из переменной окружения и id из ответа равны
    assert str(target_menu_id) == str(response_data["id"])
    # Проверка, что submenus_count из переменной окружения и submenus_count из ответа равны
    assert 1 == response_data["submenus_count"]

def test_get_submenu():
    # Отправка GET-запроса для получения информации о подменю
    response = client.get(f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
    # Проверка, что статус ответа - 200 OK
    assert response.status_code == 200
    # Получение данных из ответа
    response_data = response.json()
    # Проверка, что id из переменной окружения и id из ответа равны
    assert str(target_submenu_id) == str(response_data["id"])
    # Проверка, что dishes_count из переменной окружения и dishes_count из ответа равны
    assert 2 == response_data["dishes_count"]


def test_delete_submenu():
    # Отправка DELETE-запроса для удаления подменю
    response = client.delete(f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}")
    # Проверка, что статус ответа - 200 OK
    assert response.status_code == 200
    
def test_get_empty_submenus_list():
    # Отправка GET-запроса для получения списка подменю
    response = client.get(f"/api/v1/menus/{target_menu_id}/submenus/")
    # Проверка, что статус ответа - 200 OK
    assert response.status_code == 200
    # Получение данных из ответа
    response_data = response.json()
    # Проверка, что ответ представляет собой пустой список
    assert response_data == []


def test_get_empty_dishes_list():
    # Отправка GET-запроса для получения списка блюд
    response = client.get(f"/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes/")
    # Проверка, что статус ответа - 200 OK
    assert response.status_code == 200
    # Получение данных из ответа
    response_data = response.json()
    # Проверка, что ответ представляет собой пустой список
    assert response_data == []


def test_get_empty_menu():
    # Отправка GET-запроса для получения информации о меню
    response = client.get(f"/api/v1/menus/{target_menu_id}")
    # Проверка, что статус ответа - 200 OK
    assert response.status_code == 200
    # Получение данных из ответа
    response_data = response.json()
    # Проверка, что id из переменной окружения и id из ответа равны
    assert str(target_menu_id) == str(response_data["id"])
    # Проверка, что submenus_count из переменной окружения и submenus_count из ответа равны
    assert 0 == response_data["submenus_count"]
    # Проверка, что dishes_count из переменной окружения и dishes_count из ответа равны
    assert 0 == response_data["dishes_count"]


def test_delete_menu():
    # Отправка DELETE-запроса для удаления меню
    response = client.delete(f"/api/v1/menus/{target_menu_id}")
    # Проверка, что статус ответа - 200 OK
    assert response.status_code == 200
    # Получение данных из ответа
    response_data = response.json()
    # Проверка, что ответ является успешным
    assert response_data["status"] == "true"


def test_get_all_menus():
    # Отправка GET-запроса для получения списка всех меню
    response = client.get("/api/v1/menus/")
    # Проверка, что статус ответа - 200 OK
    assert response.status_code == 200
    # Получение данных из ответа
    response_data = response.json()
    # Проверка, что ответ является пустым списком
    assert response_data == []
