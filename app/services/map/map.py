import folium
from folium.plugins import Fullscreen, MiniMap

from app import settings
from app.services.location.helpers import get_db_locations


START_COORDS = (64.6863136, 97.7453061)
START_ZOOM = 4


class Map:
    """Класс формирования карты."""

    def __init__(self, point: tuple, zoom: int):
        """Инициализация параметров карты."""
        self.point = point
        self.zoom = zoom
        self.width = "90%"
        self.height = "80%"
        self.left = "5%"
        self.map = folium.Map(
            location=self.point,
            zoom_start=self.zoom,
            width=self.width,
            left=self.left,
            height=self.height,
        )

    def configure(self):
        """Настройки карты."""
        minimap = MiniMap()
        self.map.add_child(minimap)
        Fullscreen(
            position="topright",
            title="Fullscreen",
            title_cancel="Back on middle screen",
        ).add_to(self.map)

    def save(self):
        """Метод сохранения карты в html."""
        self.configure()
        self.map.save("{base_dir}/templates/inc/map.html".format(base_dir=settings.BASE_DIR))

    def get_marker(
        self,
        location: str,
        point: tuple,
    ):
        """Установка маркера точки."""
        marker = folium.Marker(
            icon=folium.Icon(color="darkred", icon="info-sign"),
            location=point,
            popup=folium.Popup(location, parse_html=True, max_width="20%"),
        )
        marker.add_to(self.map)
        return self

    async def get_radius_markers(
        self,
        location: str,
        point: tuple,
        radius: str,
    ):
        """Установка маркеров ближаших точек по радиусу."""
        points = await get_db_locations(location, point, float(radius))

        for point in points:
            lat, lon = point.get_lat_lon().values()
            self.get_marker(point.location, (lat, lon))
        return self
