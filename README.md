Магазин радиофармпрепаратов и медицнских изделей.
## Описание
### Технологии
- **Django**
- **React**
- **Docker**
- **Nginx**

### Авторы
Nikki Nikonor

### Выполнить миграции:
```
        cd backend
        python manage.py makemigrations
        python manage.py migrate
```

### Запустить проект:
```
        cd backend
        python manage.py runserver
```

### Создать суперпользователя:
```
        cd backend
        python manage.py createsuperuser
```

## Запуск докер контейнеров на локальной машине:

### Билдим проект и запускаем:
```
        docker compose up --build
```

### Выполнить Собрать статику Django:
```
    backend python manage.py collectstatic
    cp -r /app/collected_static/. /backend_static/static/
    cp -r /backend/collected_static/. //backend_static//static/   

```
