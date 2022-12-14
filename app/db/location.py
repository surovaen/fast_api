from geoalchemy2 import Geometry, shape
from sqlalchemy import Column, Integer, String

from app.core.models import SqlBaseModel


class Location(SqlBaseModel):
    """Локация."""

    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    location = Column(
        String,
        nullable=False,
        unique=True,
    )
    point = Column(
        Geometry(
            geometry_type="POINT",
            srid=4326,
        ),
        nullable=False,
    )

    def get_lat_lon(self) -> dict:
        """Получение latitude и longitude объекта локации."""
        point = shape.to_shape(self.point)
        return {"lon": point.x, "lat": point.y}
