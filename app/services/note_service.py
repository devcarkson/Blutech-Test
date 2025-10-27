from app.models.note import Note
from app.database import get_collection
from bson import ObjectId
from typing import List

class NoteService:
    @staticmethod
    async def create_note(note: Note) -> Note:
        collection = get_collection("notes")
        note_dict = note.model_dump(by_alias=True)
        # Remove id if it's None to let MongoDB generate it
        if note_dict.get("_id") is None:
            del note_dict["_id"]
        result = await collection.insert_one(note_dict)
        note.id = str(result.inserted_id)
        return note

    @staticmethod
    async def get_note(note_id: str, org_id: str = None) -> Note:
        collection = get_collection("notes")
        query = {"_id": ObjectId(note_id)}
        if org_id:
            query["org_id"] = org_id
        note = await collection.find_one(query)
        if not note:
            return None
        note["_id"] = str(note["_id"])
        return Note(**note)

    @staticmethod
    async def list_notes_by_org(org_id: str) -> List[Note]:
        collection = get_collection("notes")
        notes = []
        async for note in collection.find({"org_id": org_id}):
            note["_id"] = str(note["_id"])
            notes.append(Note(**note))
        return notes

    @staticmethod
    async def delete_note(note_id: str, org_id: str) -> bool:
        collection = get_collection("notes")
        result = await collection.delete_one({"_id": ObjectId(note_id), "org_id": org_id})
        return result.deleted_count > 0