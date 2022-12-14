import aiohttp

from app.core.gateway_exceptions import EXCEPTION_STATUS_MAPPING


class GatewayResponse(aiohttp.ClientResponse):
    """Базовый класс респонса, клиентской части aiohttp."""

    def raise_for_status(self) -> None:
        """Переопределение вызова Exception при ошибочных статусах."""
        if not self.ok:
            assert self.reason is not None  # noqa: S101
            self.release()
            raise EXCEPTION_STATUS_MAPPING.get(self.status, aiohttp.ClientResponseError)(
                self.request_info,
                self.history,
                status=self.status,
                message=self.reason,
                headers=self.headers,
            )
