from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, timezone

class Note(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )

    id: Optional[str] = Field(default=None, alias="_id")
    org_id: str
    title: str
    content: str
    created_by: str  # user_id
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))