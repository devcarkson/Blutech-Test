from fastapi import APIRouter, HTTPException
from app.models.organization import Organization
from app.services.organization_service import OrganizationService
from typing import List

router = APIRouter()

@router.post(
    "/",
    response_model=Organization,
    summary="Create Organization",
    description="Create a new organization in the system.",
    responses={
        200: {
            "description": "Organization created successfully"
        }
    }
)
async def create_organization(org: Organization):
    """
    Create a new organization.

    **Request Body:**
    - **name** (str): Name of the organization

    **Returns:** Organization object with generated ID and creation timestamp
    """
    return await OrganizationService.create_organization(org)

@router.get(
    "/",
    response_model=List[Organization],
    summary="List Organizations",
    description="Retrieve a list of all organizations in the system.",
    responses={
        200: {
            "description": "List of organizations"
        }
    }
)
async def list_organizations():
    """
    Get all organizations.

    **Returns:** List of all organizations with their details
    """
    return await OrganizationService.list_organizations()