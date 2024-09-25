## Тестовое задние для Brandquad

# Инстрцкуия запуска


- Клонировать репозиторий с помощью ```git clone ```

- Запустить docker-compose с помощью команды 
```bash
docker compose up --build
```

- Далее необходимо провести миграции для БД. Сделать это нужно во втором терминале по
пути ```docker-compose.yml``` с помощью команды
```bash
docker-compose exec -it backend bash
```
Откроется терминал контейнера bakcend. Здесь мы уже выполоняем команду
```bash
python manage.py migrate
```

- В этом же терминале необходимо создать суперпользлвателя для работы с админкой
```bash
python manage.py createsuperuser
```