import fastapi

from api.models.recent_pakage_model import RecentPackageModel, RecentPackage
from models.package import Package
from services import package_service

# api/packages/recent/{count}
# api/packages/details/{package_name}


router = fastapi.APIRouter()


@router.get("/api/packages/recent/{count}", response_model=RecentPackageModel)
async def recent(count: int):
    count = max(1, count)
    packages = await package_service.recently_updated_package(count)

    package_models = [RecentPackage(package_name=p.id, last_updated=p.last_updated) for p in packages]

    model = RecentPackageModel(count=count, packages=package_models)

    return model

@router.get("/api/packages/details/{package_name}", response_model=Package)
async def details(package_name: str):
    package = await package_service.search_package_by_name(package_name)
    if package is None:
        return fastapi.responses.JSONResponse({'error': f'Package {package_name} not Found'}, status_code=404)
    return package
