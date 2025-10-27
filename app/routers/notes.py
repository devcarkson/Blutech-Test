from fastapi import APIRouter, HTTPException, Depends, Request
from app.models.note import Note
from app.services.note_service import NoteService
from app.middleware.auth import get_current_user, check_permission
from typing import List

router = APIRouter()

@router.post(
    "/",
    response_model=Note,
    summary="Create Note",
    description="Create a new note. Requires writer or admin role.",
    responses={
        200: {
            "description": "Note created successfully"
        },
        403: {
            "description": "Insufficient permissions"
        }
    }
)
async def create_note(note: Note, request: Request, user=Depends(get_current_user)):
    """
    Create a new note in the user's organization.

    **Authentication Required:** X-Org-ID and X-User-ID headers

    **Permissions:** writer, admin

    **Request Body:**
    - **title** (str): Note title
    - **content** (str): Note content

    **Returns:** Complete note object with generated ID and timestamps
    """
    check_permission(user, ["writer", "admin"])
    note.org_id = user["org_id"]
    note.created_by = str(user["_id"])
    return await NoteService.create_note(note)

@router.get(
    "/",
    response_model=List[Note],
    summary="List Notes",
    description="Retrieve all notes for the user's organization.",
    responses={
        200: {
            "description": "List of notes"
        }
    }
)
async def list_notes(request: Request, user=Depends(get_current_user)):
    """
    Get all notes for the authenticated user's organization.

    **Authentication Required:** X-Org-ID and X-User-ID headers

    **Returns:** List of all notes in the organization
    """
    return await NoteService.list_notes_by_org(user["org_id"])

@router.get(
    "/{note_id}",
    response_model=Note,
    summary="Get Note",
    description="Retrieve a specific note by ID.",
    responses={
        200: {
            "description": "Note details"
        },
        404: {
            "description": "Note not found"
        }
    }
)
async def get_note(note_id: str, request: Request, user=Depends(get_current_user)):
    """
    Get a specific note by its ID.

    **Authentication Required:** X-Org-ID and X-User-ID headers

    **Path Parameters:**
    - **note_id** (str): Unique identifier of the note

    **Returns:** Complete note object
    """
    note = await NoteService.get_note(note_id, user["org_id"])
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete(
    "/{note_id}",
    summary="Delete Note",
    description="Delete a note. Requires admin role.",
    responses={
        200: {
            "description": "Note deleted successfully"
        },
        403: {
            "description": "Insufficient permissions"
        },
        404: {
            "description": "Note not found"
        }
    }
)
async def delete_note(note_id: str, request: Request, user=Depends(get_current_user)):
    """
    Delete a note by its ID.

    **Authentication Required:** X-Org-ID and X-User-ID headers

    **Permissions:** admin only

    **Path Parameters:**
    - **note_id** (str): Unique identifier of the note to delete

    **Returns:** Success message
    """
    check_permission(user, ["admin"])
    deleted = await NoteService.delete_note(note_id, user["org_id"])
    if not deleted:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted"}