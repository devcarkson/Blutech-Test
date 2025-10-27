from app.models.user import User
from app.database import get_collection
from bson import ObjectId
from typing import List

class UserService:
    @staticmethod
    async def create_user(user: User) -> User:
        collection = get_collection("users")
        user_dict = user.model_dump(by_alias=True)
        # Remove id if it's None to let MongoDB generate it
        if user_dict.get("_id") is None:
            del user_dict["_id"]
        result = await collection.insert_one(user_dict)
        user.id = str(result.inserted_id)
        return user

    @staticmethod
    async def get_user(user_id: str, org_id: str = None) -> User:
        collection = get_collection("users")
        query = {"_id": ObjectId(user_id)}
        if org_id:
            query["org_id"] = org_id
        user = await collection.find_one(query)
        if not user:
            return None
        user["_id"] = str(user["_id"])
        return User(**user)

    @staticmethod
    async def list_users_by_org(org_id: str) -> List[User]:
        collection = get_collection("users")
        users = []
        async for user in collection.find({"org_id": org_id}):
            user["_id"] = str(user["_id"])
            users.append(User(**user))
        return users