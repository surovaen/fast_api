from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse
from starlette import status

from app.core.gateway_exceptions import GATEWAY_EXCEPTIONS, NoResultException
from app.models.location import (
    LocationModel,
    RadiusLocationModel,
    RequestLocationModel,
)
from app.services.dadata.dadata_gateway import DadataGateway
from app.services.location.helpers import get_db_locations, get_found_locations


router = APIRouter()


@router.post(
    "/locations",
    summary="Запрос геоданных по адресу и ближайших городов по радиусу.",
)
async def locations(location: RequestLocationModel):
    """Обработка запроса на получение геоданных адреса."""
    try:
        search_location = await DadataGateway(location.location).execute()
        radius = location.radius
        if radius:
            search_points = search_location.get_point()
            locations = await get_db_locations(
                search_location.location,
                search_points,
                radius,
            )

            found_locations = get_found_locations(locations, search_location.location)
            response_locations = RadiusLocationModel(
                search_location=search_location,
                radius=radius,
                found_locations=[LocationModel(**loc) for loc in found_locations],
            )
            return JSONResponse(content=response_locations.dict())
        return JSONResponse(content=search_location.dict())
    except NoResultException as e:
        return JSONResponse(content={"location": e.message()})
    except GATEWAY_EXCEPTIONS:
        return Response(status_code=status.HTTP_400_BAD_REQUEST)
