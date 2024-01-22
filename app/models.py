from uuid import uuid4
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

Base = declarative_base()


class Menu(Base):
    """
    Модель для представления меню в ресторане.

    :param id: Уникальный идентификатор меню.
    :param title: Название меню.
    :param description: Описание меню.
    :param submenus: Связь с подменю в базе данных.
    """
    
    __tablename__ = "menus"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    title = Column(String, index=True)
    description = Column(String)

    submenus = relationship("Submenu", back_populates="menu", cascade="all, delete-orphan")

    @hybrid_property
    def submenus_count(self):
        return len(self.submenus)

    @hybrid_property
    def dishes_count(self):
        return sum(submenu.dishes_count for submenu in self.submenus)


class Submenu(Base):
    """
    Модель для представления подменю в ресторане.

    :param id: Уникальный идентификатор подменю.
    :param title: Название подменю (уникальное в пределах меню).
    :param description: Описание подменю.
    :param menu_id: Идентификатор связанного меню.
    :param menu: Связь с меню в базе данных.
    :param dishes: Связь с блюдами в базе данных.
    """

    __tablename__ = "submenus"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    description = Column(String)
    title = Column(String, unique=True)
    menu_id = Column(String, ForeignKey("menus.id"))

    menu = relationship("Menu", back_populates="submenus")
    dishes = relationship("Dish", back_populates="submenu", cascade="all, delete-orphan")

    @hybrid_property
    def dishes_count(self):
        return len(self.dishes)


class Dish(Base):
    """
    Модель для представления блюда в ресторане.

    :param id: Уникальный идентификатор блюда.
    :param title: Название блюда (уникальное в пределах подменю).
    :param description: Описание блюда.
    :param price: Цена блюда.
    :param menu_id: Идентификатор связанного меню.
    :param submenu_id: Идентификатор связанного подменю.
    :param submenu: Связь с подменю в базе данных.
    """

    __tablename__ = "dishes"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    title = Column(String, unique=True)
    description = Column(String)
    price = Column(String)
    menu_id = Column(String, ForeignKey("menus.id"))
    submenu_id = Column(String, ForeignKey("submenus.id"))

    submenu = relationship("Submenu", back_populates="dishes")

    @hybrid_property
    def dish_price(self):
        return f"{Dish.price:.2f}"

    def __repr__(self):
        return f"<Dish {self.title}>"
