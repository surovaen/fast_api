from aiohttp import ClientResponse, ClientSession

from app import settings
from app.core.gateway import BaseHTTPGateway
from app.core.gateway_exceptions import NoResultException
from app.core.gateway_response import GatewayResponse
from app.models.location import LocationModel


class DadataGateway(BaseHTTPGateway):
    """Класс взаимодействия с dadata."""

    headers: dict = {
        "Content-type": "application/json",
        "Authorization": "Token {token}".format(token=settings.API_KEY),
        "X-Secret": "{secret}".format(secret=settings.SECRET_KEY),
    }
    method: str = "POST"
    url: str = settings.DADATA_URL
    model = LocationModel

    def __init__(self, location: str):
        """Инициализация параметра location."""
        self.data = [location]

    def _request_params(self) -> dict:
        """Формирование аргументов запроса."""
        params = {
            "method": self.method,
            "headers": self.headers,
            "url": self.url,
            "json": self.data,
        }
        return params

    async def execute(self) -> LocationModel:
        """Метод выполнения запроса."""
        params = self._request_params()
        async with self._get_session() as session:
            async with session.request(
                raise_for_status=True,
                **params,
            ) as response:
                return await self.process_response(response)

    async def process_response(self, response: ClientResponse) -> LocationModel:
        """Метод обработки респонса к dadata."""
        response_json = await response.json()
        result = response_json[0]
        if result["result"] is None:
            raise NoResultException
        location = result["city"] or result["settlement"] or result["region"]
        return self.model(
            location=location,
            lat=float(result["geo_lat"]),
            lon=float(result["geo_lon"]),
        )

    def _get_session(self) -> ClientSession:
        """Получение экземпляра сессии."""
        return ClientSession(response_class=GatewayResponse)
