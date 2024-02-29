import datetime



from pymongo.results import UpdateResult

from models.package import Package, Release
from models.release_analytisc import ReleaseAnalytics

from beanie.odm.operators.update import array
from beanie.odm.operators.update.general import Inc
from beanie.odm.operators.update.general import Set

async def package_count() -> int:
    return await Package.count()


async def release_count() -> int:
    analytics = await ReleaseAnalytics.find_one()
    if not analytics:
        print("ERROR: No analytics?")
        return 0
    return analytics.total_releases


async def recently_updated(count=5):
    updated = await Package.find_all().sort(-Package.last_updated).limit(count).to_list()
    return updated

async def package_by_name(name: str) -> Package:
    package = await Package.find_one(Package.id == name)
    return package


async def packages_with_version(major: int, minor: int, build: int) -> int:

    # Bad way of searching releases as embeded document this is something like or. Need to use $elemMatch
    # packages_count = await Package.find(
    #     Package.releases.major_ver == major,
    #     Package.releases.minor_ver == minor,
    #     Package.releases.build_ver == build,
    #
    # )
    from beanie.odm.operators.find.array import ElemMatch
    packages_count = await Package.find(
        ElemMatch(
            Package.releases,
            {"major_ver": major, "minor_ver": minor, "build_ver": build}
        )

    ).count()

    return packages_count


async def create_release(major: int, minor: int, build: int, name: str, comment: str, size: int, url: str | None):

    release = Release(
        major_ver=major, minor_ver=minor, build_ver=build, comment=comment, url=url, size=size
    )

    update_result: UpdateResult = await Package.find_one(Package.id == name).update(
        array.Push({Package.releases: release}),
        Set({Package.last_updated: datetime.datetime.now()})
    )

    if update_result.modified_count < 1:
        raise Exception(f"No package with {name}")

    # update separate counter in release_analytics document
    await ReleaseAnalytics.find_one().update(
        Inc({ReleaseAnalytics.total_releases: 1})
    )


# Fine, but less efficient
# async def create_release(major: int, minor: int, build: int, name: str, comment: str, size: int, url: str | None):
#
#     package = await package_by_name(name)
#     if package is None:
#         raise Exception(f"No package with {name}")
#
#     release = Release(
#         major_ver=major, minor_ver=minor, build_ver=build, comment=comment, url=url, size=size
#     )
#     package.last_updated = datetime.datetime.now()
#     package.releases.append(release)
#     await package.save()
#
#     # update separate counter in release_analytics document
#     analytics = await ReleaseAnalytics.find_one()
#     analytics.total_releases += 1
#     await analytics.save()


