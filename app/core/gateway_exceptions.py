from aiohttp import ClientResponseError


class UnauthorizedException(ClientResponseError):
    """Ошибка авторизации 401 статус."""


class BadRequestException(ClientResponseError):
    """400 Ошибка валидности запроса."""


class PermissionGatewayException(ClientResponseError):
    """403 Ошибка недостаточно прав для выполнения запроса."""


class BadGatewayException(ClientResponseError):
    """502 ошибка сервера."""


class GatewayTimeoutException(ClientResponseError):
    """504 ошибка сервера."""


class InternalServerErrorException(ClientResponseError):
    """500 ошибка сервера."""


class NoResultException(Exception):
    """Отсутствует результат."""

    @staticmethod
    def message():
        """Текст ошибки."""
        return "К сожалению, адрес не найден. Попробуйте еще раз"


EXCEPTION_STATUS_MAPPING = {
    401: UnauthorizedException,
    400: BadRequestException,
    403: PermissionGatewayException,
    502: BadGatewayException,
    504: GatewayTimeoutException,
    500: InternalServerErrorException,
}

GATEWAY_EXCEPTIONS = tuple(EXCEPTION_STATUS_MAPPING.values())
