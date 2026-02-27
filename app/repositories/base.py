from bson import ObjectId
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.results import UpdateResult

from app.models.base import BaseMongoModel
from app.utils.datetime_utils import utcnow


class BaseRepository:
    model: BaseMongoModel

    def __init__(self, collection: AsyncCollection):
        self.collection = collection

    async def create(self, obj: BaseMongoModel) -> ObjectId:
        obj.created_at = utcnow()
        obj.updated_at = utcnow()

        result = await self.collection.insert_one(obj.model_dump())
        return result.inserted_id

    async def update(self, id: ObjectId, obj: BaseMongoModel) -> UpdateResult:
        obj.updated_at = utcnow()

        result = await self.collection.update_one({"_id": id}, {"$set": obj.model_dump()})
        return result

    async def find_all(self, **filters) -> list[BaseMongoModel]:
        if filters:
            cursor = self.collection.find(filters)
        else:
            cursor = self.collection.find({})
        results = await cursor.to_list(length=None)
        return [self.model.model_validate(result) for result in results]

    async def delete_all(self, **filters) -> None:
        if filters:
            await self.collection.delete_many(filters)
        else:
            await self.collection.delete_many({})

    async def find_by_id(self, id: ObjectId) -> BaseMongoModel | None:
        result = await self.collection.find_one({"_id": id})
        if result:
            return self.model.model_validate(result)
        return None

    async def find_one(self, **filters) -> BaseMongoModel | None:
        result = await self.collection.find_one(filters)
        if result:
            return self.model.model_validate(result)
        return None