from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, timezone

class Organization(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )

    id: Optional[str] = Field(default=None, alias="_id")
    name: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))