
- Проект на FastAPI с использованием PostgreSQL в качестве БД. В проекте реализован REST API по работе с меню ресторана, все CRUD операции.

## Установка

### Запуск приложения (на Windows)

- Клонировать репозиторий

```
git clone https://github.com/edgar1148/y_lab1.git
```

- Установить и активировать виртуальное окружение

```
python -m venv venv
```

```
source venv/Scripts/activate
```

- Установить зависимости requirements.txt

```
pip install -r requirements.txt
```

- Отдельный контейнер для тестов

```
docker-compose -f docker-compose-test.yml up
```

- Для запуска приложения

```
docker compose up
```


## Возможности приложения:

### Написано в соответствии с ТЗ из файла test_task.txt

#### URL для меню:
- GET /menus - получение всех меню
- POST /menus - создание меню
- GET /menus/{menu_id} - подробная информация о конкретном меню
- PATCH /menus/{menu_id} - обновление конкретного меню
- DELETE /menus/{menu_id} - удаление конкретного меню

**Для каждого меню добавлено кол-во подменю и блюд в этом меню**
- submenus_count
- dishes_count

#### URL для подменю:
- GET /menus/{menu_id}/submenus - получение всех подменю конкретного меню
- POST /menus/{menu_id}/submenus - создание подменю
- GET /menus/{menu_id}/submenus/{submenu_id} - подробная информация о конкретном подменю
- PATCH /menus/{menu_id}/submenus/{submenu_id} - обновление конкретного подменю
- DELETE /menus/{menu_id}/submenus/{submenu_id} - удаление конкретного подменю

**Для каждого подменю добавлено кол-во блюд в этом подменю**
- dishes_count

#### URL для блюд:
- GET /menus/{menu_id}/submenus/{submenu_id}/dishes - получение всех блюд
- POST /menus/{menu_id}/submenus/{submenu_id}/dishes - создание блюда
- GET /menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id} - подробная информация о конкретном блюде
- PATCH /menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id} - обновление конкретного блюда
- DELETE /menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id} - удаление конкретного блюда


#### Технологии
- fastapi==0.109.0
- psycopg2==2.9.9
- pydantic==2.5.3
- SQLAlchemy==2.0.25


#### Автор
[Евгений Екишев - edgar1148](https://github.com/edgar1148)
