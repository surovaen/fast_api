from sqlalchemy.orm import declared_attr

from app.core.crud import CRUDBase
from app.database import Base


class SqlBaseModel(Base):
    """Базовый класс модели БД."""

    __abstract__ = True

    @declared_attr
    def manager(cls) -> CRUDBase:
        """Получение менеджера ORM."""
        return CRUDBase(cls)
