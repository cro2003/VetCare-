from pydantic import BaseModel, Field
from typing import Annotated, Optional

class ChatMessage(BaseModel):
    message: Annotated[str, Field(max_length=100)]
    pet_id: Optional[str] = Field(default=None)

class TextMessages(BaseModel):
    message: Annotated[str, Field(max_length=500)]