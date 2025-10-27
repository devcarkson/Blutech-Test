import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from app.database import connect_to_mongo, close_mongo_connection
from app.database import get_collection
from bson import ObjectId

@pytest.mark.asyncio
async def test_create_note():
    await connect_to_mongo()
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
            # Create org
            org_response = await client.post("/organizations/", json={"name": "Test Org"})
            assert org_response.status_code == 200
            org_data = org_response.json()
            org_id = org_data["_id"]

            # Create user
            user_response = await client.post(f"/organizations/{org_id}/users/", json={
                "org_id": org_id,
                "name": "Test User",
                "email": "test@example.com",
                "role": "writer"
            })
            assert user_response.status_code == 200
            user_data = user_response.json()
            user_id = user_data["_id"]

            # Create note
            response = await client.post("/notes/", json={
                "org_id": org_id,
                "title": "Test Note",
                "content": "Test content",
                "created_by": user_id
            }, headers={"X-Org-ID": org_id, "X-User-ID": user_id})

            assert response.status_code == 200
            data = response.json()
            assert data["title"] == "Test Note"
            assert data["org_id"] == org_id
    finally:
        await close_mongo_connection()

@pytest.mark.asyncio
async def test_list_notes():
    await connect_to_mongo()
    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as client:
            # Create org
            org_response = await client.post("/organizations/", json={"name": "Test Org"})
            assert org_response.status_code == 200
            org_data = org_response.json()
            org_id = org_data["_id"]

            # Create user
            user_response = await client.post(f"/organizations/{org_id}/users/", json={
                "org_id": org_id,
                "name": "Test User",
                "email": "test@example.com",
                "role": "reader"
            })
            assert user_response.status_code == 200
            user_data = user_response.json()
            user_id = user_data["_id"]

            # List notes (should be empty)
            response = await client.get("/notes/", headers={"X-Org-ID": org_id, "X-User-ID": user_id})
            assert response.status_code == 200
            assert response.json() == []
    finally:
        await close_mongo_connection()