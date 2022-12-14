from typing import List

from app.database import async_session
from app.db.location import Location


async def get_db_locations(
    location: str,
    point: tuple,
    radius: float,
) -> List[Location]:
    """Получение объектов Location из БД по радиусу."""
    async with async_session() as session:
        result = await Location.manager.filter_points(
            session=session,
            location=location,
            point=point,
            radius=radius,
        )
    return result


def get_found_locations(locations: List[Location], search_location: str) -> List[dict]:
    """Получение списка словарей с аттрибутами локации."""
    found_locations = []
    for location in locations:
        if location.location != search_location:
            point = location.get_lat_lon()
            point["location"] = location.location
            found_locations.append(point)

    return found_locations
