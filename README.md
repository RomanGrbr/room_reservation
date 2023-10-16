# room_reservation

Запуск с перезапуском
uvicorn main:app --reload

Инициализация Alembic
alembic init --template async alembic

Создание файла миграции (будет создан шаблонный файл миграций без команд на изменение базы)
alembic revision

Автогенерация миграций
alembic revision --autogenerate

Фиксированный Revision ID
alembic revision --autogenerate -m "Initial structure" --rev-id 01

Применить миграции
alembic upgrade

Выполнение всех неприменённых миграций
alembic upgrade head

Отмена миграций
alembic downgrade

все миграции в хронологическом порядке
alembic history
alembic history -v

Посмотреть последнюю применённую миграцию
alembic current

вывести метку актуальной миграции
alembic history -i

FastAPI Users с SQLAlchemy
pip install "fastapi-users[sqlalchemy]==10.0.6"
