from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
# Конвертирует в JSON-формат как объекты из базы данных, так и Pydantic-модели
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
# Класс асинхронной сессии для аннотаций.
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.db import Base

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый класс CRUD операций"""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(
            self, obj_id: int, session: AsyncSession
    ) -> Optional[ModelType]:
        """Получить запись по id"""
        # db_obj = await session.execute(self.model, obj_id)
        db_obj = await session.execute(select(self.model).where(
            self.model.id == obj_id
        ))
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession) -> List[ModelType]:
        """Получить все записи"""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self, obj_in: CreateSchemaType, session: AsyncSession
    ) -> ModelType:
        """Создать запись"""
        obj_in_data = obj_in.dict()  # Конвертируем объект в словарь.
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)  # Добавляем созданный объект в сессию.
        await session.commit()  # Записываем изменения непосредственно в БД.
        # Обновляем объект, считываем данные из БД, чтобы получить его id.
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj: ModelType,
            obj_in: UpdateSchemaType,
            session: AsyncSession
    ) -> ModelType:
        """Обновить запись"""
        obj_data = jsonable_encoder(db_obj)  # конвертировать в JSON-формат
        # Перевести в словарь и исключить поля,
        # которые не были установлены пользователем.
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self, db_obj: ModelType, session: AsyncSession
    ) -> ModelType:
        """Удалить запись"""
        await session.delete(db_obj)
        await session.commit()
        # Не обновляем объект через метод refresh(),
        # следовательно он всё ещё содержит информацию об удаляемом объекте.
        return db_obj

    async def get_by_attribute(
            self, attr_name: str, attr_value: str, session: AsyncSession,
    ) -> ModelType:
        """Получить объект по произвольному атрибуту"""
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().first()
