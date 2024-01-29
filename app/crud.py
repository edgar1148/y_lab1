from sqlalchemy.orm import Session
from app.models import Menu, Submenu, Dish
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import aliased
from sqlalchemy import func

Base = declarative_base()


def create_object(db: Session, model: Base, data: dict, **kwargs):
    """
    Создает объект модели в базе данных.

    :param db: Сессия базы данных.
    :param model: Класс модели.
    :param data: Данные для создания объекта.
    :param kwargs: Дополнительные аргументы для создания объекта.
    :return: Созданный объект модели.
    """
    db_object = model(**data, **kwargs)
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object


def create_menu(db: Session, menu: dict):
    """
    Создает меню в базе данных.
    """
    return create_object(db, Menu, menu)


def create_submenu(db: Session, menu_id: str, submenu: dict):
    """
    Создает подменю в базе данных.
    """
    return create_object(db, Submenu, submenu, menu_id=menu_id)


def create_dish(db: Session, menu_id: str, submenu_id: str, dish_data: dict):
    """
    Создает блюдо в базе данных.
    """
    return create_object(db, Dish, dish_data, menu_id=menu_id, submenu_id=submenu_id)


def get_all_menus(db: Session):
    """
    Получает все меню из базы данных.
    """
    return db.query(Menu).all()


def get_menu(db: Session, menu_id: str):
    """
    Получает данные о конкретном меню из базы данных.

    :param db: Сессия базы данных.
    :param menu_id: Идентификатор меню.
    :return: Данные о меню.
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first()

    if menu:
        menu_data = {
            "id": menu.id,
            "title": menu.title,
            "description": menu.description,
            "submenus_count": len(menu.submenus),
            "dishes_count": sum(submenu.dishes_count for submenu in menu.submenus)
        }
        
        return menu_data
    else:
        return None


def get_all_submenus(db: Session):
    """
    Получает все подменю из базы данных.
    """
    return db.query(Submenu).all()


def get_submenu(db: Session, submenu_id: str):
    """
    Получает данные о конкретном подменю из базы данных.

    :param db: Сессия базы данных.
    :param submenu_id: Идентификатор подменю.
    :return: Данные о подменю.
    """
    submenu = db.query(Submenu).filter(Submenu.id == submenu_id).first()

    if submenu:
        submenu_data = {
            "id": submenu.id,
            "title": submenu.title,
            "description": submenu.description,
            "dishes_count": len(submenu.dishes)
        }

        return submenu_data
    else:
        return None


def get_all_dishes(db: Session, submenu_id: str):
    """
    Получает все блюда из базы данных для конкретного подменю.
    """
    return db.query(Dish).filter(Dish.submenu_id == submenu_id).all()


def get_dishes(db: Session, submenu_id: str):
    """
    Получает данные о конкретном блюде из базы данных.
    """
    return db.query(Dish).filter(Dish.submenu_id == submenu_id).first()


def update_object(db: Session, model: Base, object_id: str, updated_data: dict):
    """
    Обновляет данные о конкретном объекте модели в базе данных.

    :param db: Сессия базы данных.
    :param model: Класс модели.
    :param object_id: Идентификатор объекта.
    :param updated_data: Обновленные данные для объекта.
    :return: Обновленный объект модели.
    """
    db_object = db.query(model).filter(model.id == object_id).first()
    if db_object:
        for key, value in updated_data.items():
            setattr(db_object, key, value)
        db.commit()
        db.refresh(db_object)
    return db_object


def update_menu(db: Session, menu_id: str, updated_data: dict):
    """
    Обновляет данные о конкретном меню в базе данных.
    """
    return update_object(db, Menu, menu_id, updated_data)


def update_submenu(db: Session, submenu_id: str, updated_data: dict):
    """
    Обновляет данные о конкретном подменю в базе данных.
    """
    return update_object(db, Submenu, submenu_id, updated_data)


def update_dish(db: Session, dish_id: str, updated_data: dict):
    """
    Обновляет данные о конкретном блюде в базе данных.
    """
    return update_object(db, Dish, dish_id, updated_data)


def delete_object(db: Session, model: Base, object_id: str):
    """
    Удаляет конкретный объект модели из базы данных.

    :param db: Сессия базы данных.
    :param model: Класс модели.
    :param object_id: Идентификатор объекта.
    :return: Словарь с информацией об удалении объекта.
    """
    db_object = db.query(model).filter(model.id == object_id).first()
    if db_object:
        db.delete(db_object)
        db.commit()
        return {
            "status": "true",
            "message": f"The {model.__tablename__.lower()} has been deleted"
        }
    return None


def delete_menu(db: Session, menu_id: str):
    """
    Удаляет конкретное меню из базы данных.
    """
    return delete_object(db, Menu, menu_id)


def delete_submenu(db: Session, submenu_id: str):
    """
    Удаляет конкретное подменю из базы данных.
    """
    return delete_object(db, Submenu, submenu_id)


def delete_dish(db: Session, dish_id: str):
    """
    Удаляет конкретное блюдо из базы данных.
    """
    return delete_object(db, Dish, dish_id)


def partial_update_object(db: Session, model: Base, object_id: str, updated_data: dict):
    """
    Частично обновляет данные о конкретном объекте модели в базе данных.

    :param db: Сессия базы данных.
    :param model: Класс модели.
    :param object_id: Идентификатор объекта.
    :param updated_data: Частично обновленные данные для объекта.
    :return: Обновленный объект модели.
    """
    db_object = db.query(model).filter(model.id == object_id).first()
    if db_object:
        for key, value in updated_data.items():
            setattr(db_object, key, value)
        db.commit()
        db.refresh(db_object)
    return db_object


def partial_update_menu(db: Session, menu_id: str, updated_data: dict):
    """
    Частично обновляет данные о конкретном меню в базе данных.
    """
    return partial_update_object(db, Menu, menu_id, updated_data)


def partial_update_submenu(db: Session, submenu_id: str, updated_data: dict):
    """
    Частично обновляет данные о конкретном подменю в базе данных.
    """
    return partial_update_object(db, Submenu, submenu_id, updated_data)


def partial_update_dish(db: Session, dish_id: str, updated_data: dict):
    """
    Частично обновляет данные о конкретном блюде в базе данных.
    """
    return partial_update_object(db, Dish, dish_id, updated_data)
