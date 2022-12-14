import abc

from aiohttp import ClientResponse


class BaseHTTPGateway(abc.ABC):
    """Интерфейс базового gateway."""

    @abc.abstractmethod
    async def execute(self):
        """Метод выполнения запроса."""

    @abc.abstractmethod
    async def process_response(self, response: ClientResponse):
        """Обработка респонса."""

    @abc.abstractmethod
    def _request_params(self):
        """Формирование аргументов запроса."""

    @abc.abstractmethod
    def _get_session(self):
        """Формирование сессии запроса."""
