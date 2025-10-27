from fastapi import APIRouter, HTTPException
from app.models.user import User
from app.services.user_service import UserService
from app.services.organization_service import OrganizationService

router = APIRouter()

@router.post(
    "/{org_id}/users/",
    response_model=User,
    summary="Create User",
    description="Create a new user within a specific organization.",
    responses={
        200: {
            "description": "User created successfully"
        },
        404: {
            "description": "Organization not found"
        }
    }
)
async def create_user(org_id: str, user: User):
    """
    Create a new user in the specified organization.

    **Path Parameters:**
    - **org_id** (str): Organization identifier

    **Request Body:**
    - **name** (str): User's full name
    - **email** (str): User's email address
    - **role** (str): User role (reader/writer/admin)

    **Returns:** User object with generated ID and creation timestamp
    """
    # Validate org exists
    org = await OrganizationService.get_organization(org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")

    user.org_id = org_id
    return await UserService.create_user(user)