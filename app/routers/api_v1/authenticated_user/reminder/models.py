from pydantic import BaseModel, Field
from typing import Annotated

class ReminderData(BaseModel):
    id: Annotated[str | None, Field(default=None, alias="_id")]
    date: Annotated[str, Field(max_length=30)]
    summary: Annotated[str, Field(max_length=100)]
    severity: Annotated[int, Field(ge=1, le=3)]