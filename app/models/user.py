from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal
from datetime import datetime, timezone

class User(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True
    )

    id: Optional[str] = Field(default=None, alias="_id")
    org_id: str
    name: str
    email: str
    role: Literal["reader", "writer", "admin"]
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))