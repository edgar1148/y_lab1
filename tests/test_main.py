import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


# Фикстура для создания тестовых данных
@pytest.fixture(scope="function")
def created_menu_data(client):
    # Создаем меню
    response = client.post("/api/v1/menus/", json={"title": "Test Menu", "description": "Test Description"})
    assert response.status_code == 201
    created_menu_data = response.json()

    # Создаем подменю
    response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/", json={"title": "Test Submenu", "description": "Test Submenu Description"})
    assert response.status_code == 201

    # Создаем блюдо
    response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_menu_data['id']}/dishes/", json={"title": "Test Dish", "description": "Test Dish Description", "price": 10.99})
    assert response.status_code == 201

    yield created_menu_data

    # Удаляем созданные данные после выполнения теста
    client.delete(f"/api/v1/menus/{created_menu_data['id']}")

# Тесты с использованием фикстур
def test_get_menus(client, test_db):
    # Тест для получения всех меню
    response = client.get("/api/v1/menus/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_menu(client, test_db):
    # Тест для создания нового меню
    response = client.post("/api/v1/menus/", json={"title": "Test Menu", "description": "Test Description"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Menu"
    assert data["description"] == "Test Description"
    assert "id" in data

def test_get_all_menus(client, test_db):
    # Тест для получения всех меню после создания
    response = client.get("/api/v1/menus/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_menu(client, test_db, created_menu_data):
    # Тест для получения конкретного меню
    response = client.get(f"/api/v1/menus/{created_menu_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Menu"
    assert data["description"] == "Test Description"

def test_update_menu(client, test_db, created_menu_data):
    # Тест для обновления меню
    response = client.put(f"/api/v1/menus/{created_menu_data['id']}", json={"title": "Updated Menu"})
    assert response.status_code == 200
    updated_data = response.json()
    assert updated_data["title"] == "Updated Menu"
    assert updated_data["description"] == "Test Description"

def test_delete_menu(client, test_db, created_menu_data):
    # Тест для удаления меню
    response = client.delete(f"/api/v1/menus/{created_menu_data['id']}")
    assert response.status_code == 200
    delete_data = response.json()
    assert delete_data["status"] == "true"

    # Проверяем, что меню удалено
    get_response = client.get(f"/api/v1/menus/{created_menu_data['id']}")
    assert get_response.status_code == 404

def test_create_submenu(client, test_db, created_menu_data):
    # Тест для создания подменю
    response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/", json={"title": "Test Submenu", "description": "Test Submenu Description"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Submenu"
    assert data["description"] == "Test Submenu Description"
    assert "id" in data

def test_get_all_submenus(client, test_db, created_menu_data):
    # Тест для получения всех подменю
    response = client.get(f"/api/v1/menus/{created_menu_data['id']}/submenus/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_submenu(client, test_db, created_menu_data):
    # Тест для получения созданного подменю
    created_submenu_data = created_menu_data['submenus'][0]
    response = client.get(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_submenu_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Submenu"
    assert data["description"] == "Test Submenu Description"

def test_update_submenu(client, test_db, created_menu_data):
    # Тест для обновления подменю
    created_submenu_data = created_menu_data['submenus'][0]
    update_response = client.put(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_submenu_data['id']}", json={"title": "Updated Submenu"})
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["title"] == "Updated Submenu"
    assert updated_data["description"] == "Test Submenu Description"

def test_delete_submenu(client, test_db, created_menu_data):
    # Тест для удаления подменю
    created_submenu_data = created_menu_data['submenus'][0]
    delete_response = client.delete(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_submenu_data['id']}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["status"] == "true"

    # Проверяем, что подменю удалено
    get_response = client.get(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_submenu_data['id']}")
    assert get_response.status_code == 404

def test_create_dish(client, test_db, created_menu_data):
    # Тест для создания блюда
    response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_menu_data['id']}/dishes/", json={"title": "Test Dish", "description": "Test Dish Description", "price": 10.99})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Dish"
    assert data["description"] == "Test Dish Description"
    assert data["price"] == "10.99"
    assert "id" in data

def test_get_all_dishes(client, test_db, created_menu_data):
    # Тест для получения всех блюд
    response = client.get(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_menu_data['id']}/dishes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_dish(client, test_db, created_menu_data):
    # Тест для получения созданного блюда
    created_dish_data = created_menu_data['dishes'][0]
    response = client.get(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_menu_data['id']}/dishes/{created_dish_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Dish"
    assert data["description"] == "Test Dish Description"
    assert data["price"] == "10.99"

def test_update_dish(client, test_db, created_menu_data):
    # Тест для обновления блюда
    created_dish_data = created_menu_data['dishes'][0]
    update_response = client.put(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_menu_data['id']}/dishes/{created_dish_data['id']}", json={"title": "Updated Dish"})
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["title"] == "Updated Dish"
    assert updated_data["description"] == "Test Dish Description"
    assert updated_data["price"] == "10.99"

def test_delete_dish(client, test_db, created_menu_data):
    # Тест для удаления блюда
    created_dish_data = created_menu_data['dishes'][0]
    delete_response = client.delete(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_menu_data['id']}/dishes/{created_dish_data['id']}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["status"] == "true"

    # Проверяем, что блюдо удалено
    get_response = client.get(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_menu_data['id']}/dishes/{created_dish_data['id']}")
    assert get_response.status_code == 404
