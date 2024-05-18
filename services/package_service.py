import datetime
from typing import Optional

import pymongo.results

from mongo_beanie.models import Package, Release, PackageTopLevel
from mongo_beanie.models import ReleaseAnalytics
from beanie.odm.operators.find.array import ElemMatch
from beanie.odm.operators.update import array
from beanie.odm.operators.update.general import Set, Inc


async def get_package_count() -> int:
    return await Package.count()


async def get_release_count()-> int:
    analytics = await ReleaseAnalytics.find_one()
    if not analytics:
        print("Error: No analytics found")
        return 0
    return analytics.total_releases


async def recently_updated_package(count=5) -> list[Package]:
    updates = await Package.find_all().sort(-Package.last_updated).limit(count).to_list()
    return updates


async def search_package_by_name(name: str,summary_only=False) -> Optional[Package] | Optional[PackageTopLevel]:
    if not name:
        return None
    name = name.strip().lower()

    query = Package.find_one(Package.id == name)

    if not summary_only:
        return await query
    else:
        return await query.project(PackageTopLevel)



async def search_package_with_release(major: int, minor: int, build: int) -> int:
    package_count = await Package.find(
        ElemMatch(
            Package.releases,
            {"major_ver": major, "minor_ver": minor, "build_ver": build})
    ).count()

    return package_count


async def create_release(package_name: str, major: int, minor: int, build: int, size: int, comment: str,
                         url: Optional[str]):
    release = Release(major_ver=major, minor_ver=minor, build_ver=build, size=size, comment=comment, url=url)
    update_result: pymongo.results.UpdateResult = await Package.find_one(Package.id == package_name).update(
        array.Push({Package.releases: release}),
        Set({Package.last_updated: datetime.datetime.utcnow()})
    )
    if update_result.modified_count < 1:
        raise Exception(f"Package {package_name} not found")

    await ReleaseAnalytics.find_one().update(Inc({ReleaseAnalytics.total_releases: 1}))
