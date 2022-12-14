from fastapi import APIRouter, FastAPI, Request
from fastapi.templating import Jinja2Templates

from app import settings
from app.core.gateway_exceptions import GATEWAY_EXCEPTIONS, NoResultException
from app.models.forms import PostLocationForm
from app.routers.api.urls import router as api_router
from app.services.dadata.dadata_gateway import DadataGateway
from app.services.map.map import START_COORDS, START_ZOOM, Map


app = FastAPI(
    debug=settings.DEBUG,
    title=settings.APP_NAME,
)

templates = Jinja2Templates(
    directory="{base_dir}/templates".format(base_dir=settings.BASE_DIR),
)

tags_metadata = [
    {
        "name": "map",
        "description": "Стартовая страница карты.",
    },
    {
        "name": "api",
        "description": "API запроса координат адреса и ближайших городов по радиусу.",
    },
]

map_router = APIRouter()


@map_router.get(
    path="/",
    status_code=200,
    summary="Карта OpenStreetMap",
)
async def start_map(request: Request):
    """Стартовая страница карты."""
    Map(point=START_COORDS, zoom=START_ZOOM).save()
    return templates.TemplateResponse("index.html", {"request": request})


@map_router.post(
    path="/",
    status_code=200,
    summary="Поиск на карте OpenStreetMap",
)
async def search_map(request: Request):
    """Отражение искомой точки на карте и ближайших точек в пределах радиуса."""
    form = PostLocationForm(request)
    await form.load_data()
    if form.is_valid():
        try:
            search_location = await DadataGateway(form.location).execute()
            points = search_location.get_point()
            Map(points, 10).get_marker(search_location.location, points).save()
            if form.radius:
                radius = form.radius
                radius_map = await Map(points, 8).get_radius_markers(
                    search_location.location,
                    points,
                    radius,
                )
                radius_map.save()
        except NoResultException as e:
            form.__dict__.get("errors").append(
                e.message(),
            )
        except GATEWAY_EXCEPTIONS:
            form.__dict__.get("errors").append(
                "К сожалению, в данный момент сервис не доступен. Попробуйте повторить запрос позже."
            )
            return templates.TemplateResponse("index.html", form.__dict__)
    return templates.TemplateResponse("index.html", form.__dict__)


app.include_router(map_router, tags=["map"])
app.include_router(api_router, prefix="/api", tags=["api"])
