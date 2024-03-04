import datetime
from typing import Optional

import beanie
import bson
import pydantic


# Embeded dont have to be beanie model
import pymongo


class Release(pydantic.BaseModel):
    major_ver: int
    minor_ver: int
    build_ver: int
    created_date: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    comment: Optional[str]
    url: Optional[str]
    size: int


class Package(beanie.Document):
    id: str
    created_date: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    last_updated: datetime.datetime = pydantic.Field(default_factory=datetime.datetime.now)
    summary: str
    description: str
    home_page: Optional[str]
    docs_url: Optional[str]
    package_url: Optional[str]
    author_name: Optional[str]
    author_email: Optional[str]
    license: Optional[str]
    releases: list[Release]
    maintainer_ids: list[beanie.PydanticObjectId]

    class Settings:
        name = 'packages'
        indexes = [
            pymongo.IndexModel(keys=[('last_updated', pymongo.DESCENDING)], name='last_updated_descending'),
            pymongo.IndexModel(keys=[('created_date', pymongo.ASCENDING)], name='create_date_ascend'),
            pymongo.IndexModel(keys=[('author_email', pymongo.ASCENDING)], name='author_email_ascend'),
            pymongo.IndexModel(keys=[('releases.created_date', pymongo.ASCENDING)], name='releases_created_date_ascend'),

            pymongo.IndexModel(keys=[("releases.major_ver", pymongo.ASCENDING)], name="releases_major"),
            pymongo.IndexModel(keys=[("releases.minor_ver", pymongo.ASCENDING)], name="releases_minor"),
            pymongo.IndexModel(keys=[("releases.build_ver", pymongo.ASCENDING)], name="releases_build"),

            # Index on elementMatch index on all 3 versions search
            pymongo.IndexModel(keys=[
                ("releases.major_ver", pymongo.ASCENDING),
                ("releases.minor_ver", pymongo.ASCENDING),
                ("releases.build_ver", pymongo.ASCENDING)
            ],
                name="releases_version_ascending"),


        ]

# Serves as projection
class PackageTopLevelOnly(pydantic.BaseModel):
    id: str
    last_updated: datetime.datetime
    summary: str

    class Settings:
        projection = {
            "id": "$_id",
            "summary": "$summary",
            "last_updated": "$last_updated",
        }
