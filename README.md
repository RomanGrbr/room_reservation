# room_reservation

Запуск с перезапуском
uvicorn main:app --reload

Инициализация Alembic
alembic init --template async alembic

Создание файла миграции (будет создан шаблонный файл миграций без команд на изменение базы)
alembic revision

Автогенерация миграций
alembic revision --autogenerate

Применить миграции
alembic upgrade

Отмена миграций
alembic downgrade
