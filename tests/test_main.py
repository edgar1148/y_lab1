import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.crud import get_menu, create_menu, get_submenu, create_submenu, get_dishes, create_dish, \
    delete_submenu, delete_dish, delete_menu

# Повторяющиеся данные
MENU_DATA = {"title": "Test Menu", "description": "Test Description"}
SUBMENU_DATA = {"title": "Test Submenu", "description": "Test Submenu Description"}
DISH_DATA = {"title": "Test Dish", "description": "Test Dish Description", "price": 10.99}


def test_create_menu(client, test_db):
    # Отправляем POST-запрос для создания меню
    response = client.post("/api/v1/menus/", json=MENU_DATA)
    assert response.status_code == 201

    # Получаем созданный объект меню из БД
    created_menu_id = response.json()["id"]
    retrieved_menu = get_menu(test_db, created_menu_id)

    # Проверяем, что объект создан
    assert retrieved_menu is not None

    # Сравниваем поля объекта в БД с полями из ответа
    assert retrieved_menu.title == response.json()["title"]
    assert retrieved_menu.description == response.json()["description"]

    # Удаляем созданный объект меню из БД
    delete_menu(test_db, created_menu_id)


def test_get_menu(client, test_db):
    # Создаем объект меню в БД с использованием ORM
    created_menu = create_menu(test_db, MENU_DATA)

    # Получаем созданный объект меню через GET-запрос
    response = client.get(f"/api/v1/menus/{created_menu.id}")
    assert response.status_code == 200

    # Проверяем, что полученное меню соответствует ожиданиям
    data = response.json()
    assert data["title"] == MENU_DATA["title"]
    assert data["description"] == MENU_DATA["description"]

    # Удаляем созданный объект меню из БД
    delete_menu(test_db, created_menu.id)


def test_update_menu(client, test_db):
    # Сначала создаем меню
    created_menu = create_menu(test_db, MENU_DATA)

    # Обновляем меню
    update_response = client.put(f"/api/v1/menus/{created_menu.id}", json={"title": "Updated Menu"})
    assert update_response.status_code == 200

    # Получаем обновленный объект меню из БД
    updated_menu = get_menu(test_db, created_menu.id)

    # Проверяем, что объект обновлен
    assert updated_menu is not None

    # Сравниваем поля объекта в БД с полями из ответа
    assert updated_menu.title == "Updated Menu"
    assert updated_menu.description == MENU_DATA["description"]

    # Удаляем созданный объект меню из БД
    delete_menu(test_db, created_menu.id)


def test_delete_menu(client, test_db):
    # Сначала создаем меню
    created_menu = create_menu(test_db, MENU_DATA)

    # Удаляем меню
    delete_response = client.delete(f"/api/v1/menus/{created_menu.id}")
    assert delete_response.status_code == 200
    delete_data = delete_response.json()
    assert delete_data["status"] == "true"

    # Проверяем, что меню удалено
    assert get_menu(test_db, created_menu.id) is None


def test_create_submenu(client, test_db):
    # Сначала создаем меню
    created_menu = create_menu(test_db, MENU_DATA)

    # Создаем подменю
    response = client.post(f"/api/v1/menus/{created_menu.id}/submenus/", json=SUBMENU_DATA)
    assert response.status_code == 201

    # Получаем созданный объект подменю из БД
    created_submenu_id = response.json()["id"]
    created_submenu = get_submenu(test_db, created_submenu_id)

    # Проверяем, что объект создан
    assert created_submenu is not None

    # Сравниваем поля объекта в БД с полями из ответа
    assert created_submenu.title == SUBMENU_DATA["title"]
    assert created_submenu.description == SUBMENU_DATA["description"]

    # Удаляем созданный объект подменю из БД
    delete_submenu(test_db, created_submenu.id)


def test_get_all_submenus(client, test_db):
    # Создаем меню и подменю
    created_menu = create_menu(test_db, MENU_DATA)
    created_submenu = create_submenu(test_db, created_menu.id, SUBMENU_DATA)

    # Получаем все подменю
    response = client.get(f"/api/v1/menus/{created_menu.id}/submenus/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

    # Удаляем созданные объекты меню и подменю из БД
    delete_submenu(test_db, created_submenu.id)
    delete_menu(test_db, created_menu.id)


def test_get_submenu(client, test_db):
    # Создаем меню и подменю
    created_menu = create_menu(test_db, MENU_DATA)
    created_submenu = create_submenu(test_db, created_menu.id, SUBMENU_DATA)

    # Получаем созданное подменю через GET-запрос
    response = client.get(f"/api/v1/menus/{created_menu.id}/submenus/{created_submenu.id}")
    assert response.status_code == 200

    # Проверяем, что полученное подменю соответствует ожиданиям
    data = response.json()
    assert data["title"] == SUBMENU_DATA["title"]
    assert data["description"] == SUBMENU_DATA["description"]

    # Удаляем созданные объекты меню и подменю из БД
    delete_submenu(test_db, created_submenu.id)
    delete_menu(test_db, created_menu.id)


def test_update_submenu(client, test_db):
    # Создаем меню и подменю
    created_menu = create_menu(test_db, MENU_DATA)
    created_submenu = create_submenu(test_db, created_menu.id, SUBMENU_DATA)

    # Обновляем подменю
    update_response = client.put(f"/api/v1/menus/{created_menu.id}/submenus/{created_submenu.id}", json={"title": "Updated Submenu"})
    assert update_response.status_code == 200

    # Проверяем, что подменю было обновлено в БД
    updated_submenu = get_submenu(test_db, created_submenu.id)
    assert updated_submenu.title == "Updated Submenu"
    assert updated_submenu.description == SUBMENU_DATA["description"]

    # Удаляем созданные объекты меню и подменю из БД
    delete_submenu(test_db, created_submenu.id)
    delete_menu(test_db, created_menu.id)


def test_delete_submenu(client, test_db):
    # Создаем меню и подменю
    created_menu = create_menu(test_db, MENU_DATA)
    created_submenu = create_submenu(test_db, created_menu.id, SUBMENU_DATA)

    # Удаляем подменю
    delete_response = client.delete(f"/api/v1/menus/{created_menu.id}/submenus/{created_submenu.id}")
    assert delete_response.status_code == 200

    # Проверяем, что подменю удалено из БД
    assert get_submenu(test_db, created_submenu.id) is None

    # Удаляем созданный объект меню из БД
    delete_menu(test_db, created_menu.id)


def test_create_dish(client, test_db):
    # Создаем меню и подменю
    created_menu = create_menu(test_db, MENU_DATA)
    created_submenu = create_submenu(test_db, created_menu.id, SUBMENU_DATA)

    # Создаем блюдо
    response = client.post(f"/api/v1/menus/{created_menu.id}/submenus/{created_submenu.id}/dishes/", json=DISH_DATA)
    assert response.status_code == 201

    # Получаем созданное блюдо из БД
    created_dish_id = response.json()["id"]
    retrieved_dish = get_dishes(test_db, created_dish_id)

    # Проверяем, что блюдо было создано
    assert retrieved_dish is not None

    # Сравниваем поля блюда в БД с полями из ответа
    assert retrieved_dish.title == DISH_DATA["title"]
    assert retrieved_dish.description == DISH_DATA["description"]
    assert retrieved_dish.price == DISH_DATA["price"]

    # Удаляем созданные объекты меню и подменю из БД
    delete_dish(test_db, created_dish_id)
    delete_submenu(test_db, created_submenu.id)
    delete_menu(test_db, created_menu.id)


def test_get_all_dishes(client, test_db):
    # Создаем меню, подменю и блюдо
    created_menu = create_menu(test_db, MENU_DATA)
    created_submenu = create_submenu(test_db, created_menu.id, SUBMENU_DATA)
    created_dish = create_dish(test_db, created_submenu.id, DISH_DATA)

    # Получаем все блюда
    response = client.get(f"/api/v1/menus/{created_menu.id}/submenus/{created_submenu.id}/dishes/")
    assert response.status_code == 200

    # Проверяем, что полученные блюда соответствуют ожиданиям
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == DISH_DATA["title"]
    assert data[0]["description"] == DISH_DATA["description"]
    assert data[0]["price"] == DISH_DATA["price"]

    # Удаляем созданные объекты меню и подменю из БД
    delete_dish(test_db, created_dish.id)
    delete_submenu(test_db, created_submenu.id)
    delete_menu(test_db, created_menu.id)


def test_get_dish(client, test_db):
    # Создаем меню, подменю и блюдо
    created_menu = create_menu(test_db, MENU_DATA)
    created_submenu = create_submenu(test_db, created_menu.id, SUBMENU_DATA)
    created_dish = create_dish(test_db, created_submenu.id, DISH_DATA)

    # Получаем созданное блюдо через GET-запрос
    response = client.get(f"/api/v1/menus/{created_menu.id}/submenus/{created_submenu.id}/dishes/{created_dish.id}")
    assert response.status_code == 200

    # Проверяем, что полученное блюдо соответствует ожиданиям
    data = response.json()
    assert data["title"] == DISH_DATA["title"]
    assert data["description"] == DISH_DATA["description"]
    assert data["price"] == DISH_DATA["price"]

    # Удаляем созданные объекты меню и подменю из БД
    delete_dish(test_db, created_dish.id)
    delete_submenu(test_db, created_submenu.id)
    delete_menu(test_db, created_menu.id)


def test_get_menus(client, test_db):
    # Создаем два объекта меню в тестовой базе данных
    menu_data = [
        {"title": "Menu 1", "description": "Description 1"},
        {"title": "Menu 2", "description": "Description 2"},
    ]

    created_menus = [create_menu(test_db, data) for data in menu_data]

    # Получаем все меню
    response = client.get("/api/v1/menus/")
    assert response.status_code == 200

    # Проверяем, что полученные данные соответствуют ожиданиям
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(menu_data)

    # Проверяем каждый объект меню
    for i, menu in enumerate(data):
        assert menu["title"] == menu_data[i]["title"]
        assert menu["description"] == menu_data[i]["description"]

    # Удаляем созданные объекты меню из БД
    for created_menu in created_menus:
        delete_menu(test_db, created_menu.id)
