import fastapi

from mongo_beanie.api.models.stats_model import StatsModel
from mongo_beanie.services import user_service, package_service

# api/packages/recent/{count}
# api/packages/details/{package_name}


router = fastapi.APIRouter()

@router.get("/api/stats",response_model=StatsModel)
async def recent(count: int = 5):
    package_count = await package_service.get_package_count()
    release_count = await package_service.get_release_count()
    user_count = await user_service.get_user_count()

    return StatsModel(package_count=package_count, release_count=release_count, user_count=user_count)
