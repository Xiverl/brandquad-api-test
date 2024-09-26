# Тестовое задние для Brandquad

## Инструкция запуска


- Клонировать репозиторий с помощью 
```bash
git clone git@github.com:Xiverl/brandquad-api-test.git
```

- Запустить docker-compose с помощью команды 
```bash
docker compose up --build
```

- Далее необходимо провести миграции для БД. Сделать это нужно во втором терминале по
пути ```docker-compose.yml``` с помощью команды
```bash
docker-compose exec -it backend bash
```

- Откроется терминал контейнера bakcend. Здесь мы уже выполоняем команду
```bash
python manage.py migrate
```

- В этом же терминале необходимо создать суперпользлвателя для работы с админкой
```bash
python manage.py createsuperuser
```



## Как запустить парсинг ссылки через Management Comand


- Откройте второй терминал по расположению docker-compose.yml и выполните команду
```bash
docker-compose exec -it backend bash
```

- Откроется терминал контейнера backend. В нем необходимо выпонить команду
```bash
python manage.py parse_log_file <ссылка_на_файл>
```



## Какие есть эндпоинты

- ```http://127.0.0.1:8000/admin``` - ```GET``` запрос который открывает админку

- ```http://127.0.0.1:8000/api/nginx-logs``` - ```GET``` запрос который выводит список логов nginx
- ```http://127.0.0.1:8000/api/nginx-logs/{id}``` - ```GET``` запрос который выводит конкретный лог nginx по id

- ```http://127.0.0.1:8000/api/nginx-logs/upload_log``` - ```POST``` запрос который парсит файл по ссылке и сохраняет данные в БД.

Формат json:
```json
{
    "file_url": "<ссылка_на_файл>"
}
```