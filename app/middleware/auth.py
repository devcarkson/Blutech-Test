from fastapi import Request, HTTPException
from app.database import get_collection
from bson import ObjectId

async def get_current_user(request: Request):
    org_id = request.headers.get("X-Org-ID")
    user_id = request.headers.get("X-User-ID")

    if not org_id or not user_id:
        raise HTTPException(status_code=401, detail="X-Org-ID and X-User-ID headers required")

    try:
        user_collection = get_collection("users")
        user = await user_collection.find_one({"_id": ObjectId(user_id), "org_id": org_id})
        if not user:
            raise HTTPException(status_code=401, detail="Invalid user or organization")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid user ID")

def check_permission(user, required_roles):
    if user["role"] not in required_roles:
        raise HTTPException(status_code=403, detail="Insufficient permissions")