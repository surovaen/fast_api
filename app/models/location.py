from typing import List, Tuple

from pydantic import BaseModel


class LocationModel(BaseModel):
    """Модель локации."""

    location: str
    lat: float
    lon: float

    def get_point(self) -> Tuple[float, float]:
        """Метод получения latitude и longitude объекта локации."""
        return self.lat, self.lon


class RadiusLocationModel(BaseModel):
    """Модель локации с ближайшими точками по радиусу."""

    search_location: LocationModel
    radius: float
    found_locations: List[LocationModel]


class RequestLocationModel(BaseModel):
    """Модель запроса в api."""

    location: str
    radius: float = None
