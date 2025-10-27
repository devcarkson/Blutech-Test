from app.models.organization import Organization
from app.database import get_collection
from bson import ObjectId
from typing import List

class OrganizationService:
    @staticmethod
    async def create_organization(org: Organization) -> Organization:
        collection = get_collection("organizations")
        org_dict = org.model_dump(by_alias=True)
        # Remove id if it's None to let MongoDB generate it
        if org_dict.get("_id") is None:
            del org_dict["_id"]
        result = await collection.insert_one(org_dict)
        org.id = str(result.inserted_id)
        return org

    @staticmethod
    async def get_organization(org_id: str) -> Organization:
        collection = get_collection("organizations")
        org = await collection.find_one({"_id": ObjectId(org_id)})
        if not org:
            return None
        org["_id"] = str(org["_id"])
        return Organization(**org)

    @staticmethod
    async def list_organizations() -> List[Organization]:
        collection = get_collection("organizations")
        orgs = []
        async for org in collection.find():
            org["_id"] = str(org["_id"])
            orgs.append(Organization(**org))
        return orgs