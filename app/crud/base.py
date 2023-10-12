from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    """Базовый класс CRUD операций"""

    def __init__(self, model):
        self.model = model

    async def get(self, obj_id: int, session: AsyncSession):
        """Получить запись по id"""
        # db_obj = await session.execute(self.model, obj_id)
        db_obj = await session.execute(select(self.model).where(
            self.model.id == obj_id
        ))
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        """Получить все записи"""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(self, obj_in, session: AsyncSession):
        """Создать запись"""
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj, obj_in, session: AsyncSession,):
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

    async def remove(self, db_obj, session: AsyncSession,):
        """Удалить запись"""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_by_attribute(
            self, attr_name: str, attr_value: str, session: AsyncSession,
    ):
        """Получить объект по произвольному атрибуту"""
        attr = getattr(self.model, attr_name)
        db_obj = await session.execute(
            select(self.model).where(attr == attr_value)
        )
        return db_obj.scalars().first()
