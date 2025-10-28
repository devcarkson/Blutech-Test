from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import connect_to_mongo, close_mongo_connection
from app.routers.organizations import router as org_router
from app.routers.users import router as user_router
from app.routers.notes import router as note_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_mongo()
    yield
    # Shutdown
    await close_mongo_connection()

app = FastAPI(
    title="Multi-Tenant Notes API",
    description="""
    A comprehensive multi-tenant notes management system built with FastAPI and MongoDB.

    Features

    1 Multi-tenant architecture: Organizations can manage their own users and notes
    2 Role-based access control: Reader, Writer, and Admin roles
    3 RESTful API**: Complete CRUD operations for organizations, users, and notes
    4 MongoDB integration: Scalable document-based storage

    Authentication

    All endpoints (except root) require authentication headers:
    1 `X-Org-ID`: Organization identifier
    2 `X-User-ID`: User identifier

    Roles & Permissions

    1 Reader: Can view notes
    2 Writer: Can create and view notes
    3 Admin: Full access including user management and note deletion
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "carksontech@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan
)

app.include_router(org_router, prefix="/organizations", tags=["organizations"])
app.include_router(user_router, prefix="/organizations", tags=["users"])
app.include_router(note_router, prefix="/notes", tags=["notes"])

@app.get("/")
async def root():
    return {"message": "Multi-Tenant Notes API"}