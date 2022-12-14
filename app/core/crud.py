from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDBase:
    """Базовый класс CRUD операций с БД."""

    def __init__(self, model):
        """Инициализация."""
        self.model = model

    async def create(
        self,
        session: AsyncSession,
        **kwargs,
    ):
        """Создать один объект в БД."""
        instance = self.model(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    async def get(
        self,
        session: AsyncSession,
        location: str,
    ):
        """Получение одного объекта."""
        query = select(self.model).where(
            self.model.location.ilike("%{location}%".format(location=location)),
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def filter_points(
        self,
        session: AsyncSession,
        location: str,
        point: tuple,
        radius: float,
    ) -> list:
        """Метод получения объектов, ближайших по радиусу."""
        loc = await self.get(session=session, location=location)
        if loc is None:
            loc = await self.create(
                session=session,
                location=location,
                point=f"POINT({point[0]} {point[1]})",
            )

        query = select(self.model).where(
            self.model.point.ST_DWithin(
                loc.point,
                radius / 111.120,
            )
        )
        result = await session.execute(query)
        return result.scalars().all()
