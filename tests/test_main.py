import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def test_get_menus(client):
    response = client.get("/api/v1/menus/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_menu(client):
    response = client.post("/api/v1/menus/", json={"title": "Test Menu", "description": "Test Description"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Menu"
    assert data["description"] == "Test Description"
    assert "id" in data

    # Уборка
    client.delete(f"/api/v1/menus/{data['id']}")


def test_get_all_menus(client):
    response = client.get("/api/v1/menus/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_menu(client):
    # Сначала создаем меню
    create_response = client.post("/api/v1/menus/", json={"title": "Test Menu", "description": "Test Description"})
    assert create_response.status_code == 201
    created_data = create_response.json()

    # Получаем созданное меню
    response = client.get(f"/api/v1/menus/{created_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Menu"
    assert data["description"] == "Test Description"

    # Уборка
    client.delete(f"/api/v1/menus/{created_data['id']}")


def test_update_menu(client):
    # Сначала создаем меню
    create_response = client.post("/api/v1/menus/", json={"title": "Test Menu", "description": "Test Description"})
    assert create_response.status_code == 201
    created_data = create_response.json()

    # Обновляем меню
    update_response = client.put(f"/api/v1/menus/{created_data['id']}", json={"title": "Updated Menu"})
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["title"] == "Updated Menu"
    assert updated_data["description"] == "Test Description"

    # Уборка
    client.delete(f"/api/v1/menus/{created_data['id']}")


def test_delete_menu(client):
    # Сначала создаем меню
    create_response = client.post("/api/v1/menus/", json={"title": "Test Menu", "description": "Test Description"})
    assert create_response.status_code == 201
    created_data = create_response.json()

    # Удаляем меню
    delete_response = client.delete(f"/api/v1/menus/{created_data['id']}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["status"] == "true"

    # Проверяем, что меню удалено
    get_response = client.get(f"/api/v1/menus/{created_data['id']}")
    assert get_response.status_code == 404


def test_create_submenu(client):
    # Сначала создаем меню
    create_menu_response = client.post("/api/v1/menus/", json={"title": "Test Menu", "description": "Test Description"})
    assert create_menu_response.status_code == 201
    created_menu_data = create_menu_response.json()

    # Создаем подменю
    response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/", json={"title": "Test Submenu", "description": "Test Submenu Description"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Submenu"
    assert data["description"] == "Test Submenu Description"
    assert "id" in data

    # Уборка
    client.delete(f"/api/v1/menus/{created_menu_data['id']}")


def test_get_all_submenus(client):
    # Сначала создаем меню и подменю
    create_menu_response = client.post("/api/v1/menus/", json={"title": "Test Menu", "description": "Test Description"})
    assert create_menu_response.status_code == 201
    created_menu_data = create_menu_response.json()

    create_submenu_response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/", json={"title": "Test Submenu", "description": "Test Submenu Description"})
    assert create_submenu_response.status_code == 201

    # Получаем все подменю
    response = client.get(f"/api/v1/menus/{created_menu_data['id']}/submenus/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    # Уборка
    client.delete(f"/api/v1/menus/{created_menu_data['id']}")


def test_get_submenu(client):
    # Сначала создаем меню и подменю
    create_menu_response = client.post("/api/v1/menus/", json={"title": "Test Menu", "description": "Test Description"})
    assert create_menu_response.status_code == 201
    created_menu_data = create_menu_response.json()

    create_submenu_response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/", json={"title": "Test Submenu", "description": "Test Submenu Description"})
    assert create_submenu_response.status_code == 201
    created_submenu_data = create_submenu_response.json()

    # Получаем созданное подменю
    response = client.get(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_submenu_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Submenu"
    assert data["description"] == "Test Submenu Description"

    # Уборка
    client.delete(f"/api/v1/menus/{created_menu_data['id']}")


def test_update_submenu(client):
    # Сначала создаем меню и подменю
    create_menu_response = client.post("/api/v1/menus/", json={"title": "Test Menu", "description": "Test Description"})
    assert create_menu_response.status_code == 201
    created_menu_data = create_menu_response.json()

    create_submenu_response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/", json={"title": "Test Submenu", "description": "Test Submenu Description"})
    assert create_submenu_response.status_code == 201
    created_submenu_data = create_submenu_response.json()

    # Обновляем подменю
    update_response = client.put(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_submenu_data['id']}", json={"title": "Updated Submenu"})
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["title"] == "Updated Submenu"
    assert updated_data["description"] == "Test Submenu Description"

    # Уборка
    client.delete(f"/api/v1/menus/{created_menu_data['id']}")


def test_delete_submenu(client):
    # Сначала создаем меню и подменю
    create_menu_response = client.post("/api/v1/menus/", json={"title": "Test Menu", "description": "Test Description"})
    assert create_menu_response.status_code == 201
    created_menu_data = create_menu_response.json()

    create_submenu_response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/", json={"title": "Test Submenu", "description": "Test Submenu Description"})
    assert create_submenu_response.status_code == 201
    created_submenu_data = create_submenu_response.json()

    # Удаляем подменю
    delete_response = client.delete(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_submenu_data['id']}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["status"] == "true"

    # Проверяем, что подменю удалено
    get_response = client.get(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_submenu_data['id']}")
    assert get_response.status_code == 404

    # Уборка
    client.delete(f"/api/v1/menus/{created_menu_data['id']}")


def test_create_dish(client):
    # Сначала создаем меню и подменю
    create_menu_response = client.post("/api/v1/menus/", json={"title": "Test Menu", "description": "Test Description"})
    assert create_menu_response.status_code == 201
    created_menu_data = create_menu_response.json()

    create_submenu_response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/", json={"title": "Test Submenu", "description": "Test Submenu Description"})
    assert create_submenu_response.status_code == 201
    created_submenu_data = create_submenu_response.json()

    # Создаем блюдо
    response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_submenu_data['id']}/dishes/", json={"title": "Test Dish", "description": "Test Dish Description", "price": 10.99})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Dish"
    assert data["description"] == "Test Dish Description"
    assert data["price"] == "10.99"
    assert "id" in data

    # Уборка
    client.delete(f"/api/v1/menus/{created_menu_data['id']}")


def test_get_all_dishes(client):
    # Сначала создаем меню, подменю и блюдо
    create_menu_response = client.post("/api/v1/menus/", json={"title": "Test Menu", "description": "Test Description"})
    assert create_menu_response.status_code == 201
    created_menu_data = create_menu_response.json()

    create_submenu_response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/", json={"title": "Test Submenu", "description": "Test Submenu Description"})
    assert create_submenu_response.status_code == 201
    created_submenu_data = create_submenu_response.json()

    create_dish_response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_submenu_data['id']}/dishes/", json={"title": "Test Dish", "description": "Test Dish Description", "price": 10.99})
    assert create_dish_response.status_code == 201

    # Получаем все блюда
    response = client.get(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_submenu_data['id']}/dishes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    # Уборка
    client.delete(f"/api/v1/menus/{created_menu_data['id']}")


def test_get_dish(client):
    # Сначала создаем меню, подменю и блюдо
    create_menu_response = client.post("/api/v1/menus/", json={"title": "Test Menu", "description": "Test Description"})
    assert create_menu_response.status_code == 201
    created_menu_data = create_menu_response.json()

    create_submenu_response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/", json={"title": "Test Submenu", "description": "Test Submenu Description"})
    assert create_submenu_response.status_code == 201
    created_submenu_data = create_submenu_response.json()

    create_dish_response = client.post(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_submenu_data['id']}/dishes/", json={"title": "Test Dish", "description": "Test Dish Description", "price": 10.99})
    assert create_dish_response.status_code == 201
    created_dish_data = create_dish_response.json()

    # Получаем созданное блюдо
    response = client.get(f"/api/v1/menus/{created_menu_data['id']}/submenus/{created_submenu_data['id']}/dishes/{created_dish_data['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Dish"
    assert data["description"] == "Test Dish Description"
    assert data["price"] == "10.99"

    # Уборка
    client.delete(f"/api/v1/menus/{created_menu_data['id']}")
