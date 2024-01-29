from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session

from app.models import Base
from app.database import SessionLocal, engine

from app.crud import (
    create_menu, create_submenu, create_dish,
    get_all_menus, get_menu, get_all_submenus, get_submenu, get_all_dishes, get_dishes,
    update_menu, update_submenu, update_dish,
    delete_menu, delete_submenu, delete_dish,
    partial_update_menu, partial_update_submenu, partial_update_dish
)
from pydantic import BaseModel

app = FastAPI()

def init_db():
    """Инициализация базы данных."""
    Base.metadata.create_all(bind=engine)

init_db()

def get_db():
    """Зависимость для получения сессии базы данных."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class MenuCreate(BaseModel):
    """Модель для создания меню."""
    title: str
    description: str

class SubmenuCreate(BaseModel):
    """Модель для создания подменю."""
    title: str
    description: str

class DishCreate(BaseModel):
    """Модель для создания блюда."""
    title: str
    description: str
    price: float

router = APIRouter()

@router.post("/api/v1/menus/", status_code=status.HTTP_201_CREATED)
def create_menu_endpoint(menu: MenuCreate, db: Session = Depends(get_db)):
    """REST API для создания меню."""
    return create_menu(db, menu.dict())

@router.post("/api/v1/menus/{menu_id}/submenus/", status_code=status.HTTP_201_CREATED)
def create_submenu_endpoint(menu_id: str, submenu: SubmenuCreate, db: Session = Depends(get_db)):
    """REST API для создания подменю."""
    return create_submenu(db, menu_id, submenu.dict())

@router.post("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/", status_code=status.HTTP_201_CREATED)
def create_dish_endpoint(menu_id: str, submenu_id: str, dish: DishCreate, db: Session = Depends(get_db)):
    """REST API для создания блюда."""
    return create_dish(db, menu_id, submenu_id, dish.dict())

@router.get("/api/v1/menus/")
def read_all_menus(db: Session = Depends(get_db)):
    """REST API для получения всех меню."""
    return get_all_menus(db)

@router.get("/api/v1/menus/{menu_id}")
def read_menu(menu_id: str, db: Session = Depends(get_db)):
    """REST API для получения меню."""
    menu = get_menu(db, menu_id)
    if menu is None:
        raise HTTPException(status_code=404, detail='menu not found')
    return menu

@router.get("/api/v1/menus/{menu_id}/submenus/")
def read_all_submenus(db: Session = Depends(get_db)):
    """REST API для получения всех подменю."""
    return get_all_submenus(db)

@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def read_submenu(submenu_id: str, db: Session = Depends(get_db)):
    """REST API для получения конкретного подменю."""
    submenu = get_submenu(db, submenu_id)
    if submenu is None:
        raise HTTPException(status_code=404, detail='submenu not found')
    return submenu

@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/")
def read_all_dishes(submenu_id: str, db: Session = Depends(get_db)):
    """REST API для получения блюд."""
    return get_all_dishes(db, submenu_id)

@router.get("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def read_dishes(menu_id: str, submenu_id: str, db: Session = Depends(get_db)):
    """REST API для получения блюда."""
    dish = get_dishes(db, submenu_id)
    if dish is None:
        raise HTTPException(status_code=404, detail='dish not found')
    return dish

@router.put("/api/v1/menus/{menu_id}")
def update_menu_endpoint(menu_id: str, updated_data: dict, db: Session = Depends(get_db)):
    """REST API для обновления меню."""
    return update_menu(db, menu_id, updated_data)

@router.put("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def update_submenu_endpoint(submenu_id: str, updated_data: dict, db: Session = Depends(get_db)):
    """REST API для обновления подменю."""
    return update_submenu(db, submenu_id, updated_data)

@router.put("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def update_dish_endpoint(dish_id: str, updated_data: dict, db: Session = Depends(get_db)):
    """REST API для обновления блюда."""
    return update_dish(db, dish_id, updated_data)

@router.delete("/api/v1/menus/{menu_id}")
def delete_menu_endpoint(menu_id: str, db: Session = Depends(get_db)):
    """REST API для удаления меню."""
    return delete_menu(db, menu_id)

@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def delete_submenu_endpoint(submenu_id: str, db: Session = Depends(get_db)):
    """REST API для удаления подменю."""
    return delete_submenu(db, submenu_id)

@router.delete("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def delete_dish_endpoint(dish_id: str, db: Session = Depends(get_db)):
    """REST API для удаления блюда."""
    return delete_dish(db, dish_id)

@router.patch("/api/v1/menus/{menu_id}")
def partial_update_menu_endpoint(menu_id: str, updated_data: dict, db: Session = Depends(get_db)):
    """REST API для частичного обновления меню."""
    return partial_update_menu(db, menu_id, updated_data)

@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}")
def partial_update_submenu_endpoint(submenu_id: str, updated_data: dict, db: Session = Depends(get_db)):
    """REST API для частичного обновления подменю."""
    return partial_update_submenu(db, submenu_id, updated_data)

@router.patch("/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
def partial_update_dish_endpoint(dish_id: str, updated_data: dict, db: Session = Depends(get_db)):
    """REST API для частичного обновления блюда."""
    return partial_update_dish(db, dish_id, updated_data)

app.include_router(router)
