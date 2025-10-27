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

    ## Features

    * **Multi-tenant architecture**: Organizations can manage their own users and notes
    * **Role-based access control**: Reader, Writer, and Admin roles
    * **RESTful API**: Complete CRUD operations for organizations, users, and notes
    * **MongoDB integration**: Scalable document-based storage

    ## Authentication

    All endpoints (except root) require authentication headers:
    - `X-Org-ID`: Organization identifier
    - `X-User-ID`: User identifier

    ## Roles & Permissions

    - **Reader**: Can view notes
    - **Writer**: Can create and view notes
    - **Admin**: Full access including user management and note deletion
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