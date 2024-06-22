from abc import ABC, abstractmethod
from sqlalchemy import insert, select, update, delete

from src.api.db import async_session_maker


class AbstractRepository(ABC):
    @abstractmethod
    async def add(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_by_options(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_options(self, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    async def add(self, data: dict) -> int:
        async with async_session_maker() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            res = await session.execute(stmt)
            await session.commit()
            return res.scalar_one()

    async def find_by_options(self, unique: bool = False, **kwargs):
        async with async_session_maker() as session:
            stmt = select(self.model).filter_by(**kwargs)
            results = await session.execute(stmt)
            if unique:
                results = results.scalar_one_or_none()
            else:
                results = results.scalars().all()
            return results

    async def update(self, data: dict, **kwargs):
        async with async_session_maker() as session:
            stmt = update(self.model).filter_by(**kwargs).values(**data)
            await session.execute(stmt)
            await session.commit()

    async def delete_by_options(self, id_character: int, **kwargs):
        async with async_session_maker() as session:
            stmt = delete(self.model).where(self.model.id.in_([id_character]))
            await session.execute(stmt)
            await session.commit()
