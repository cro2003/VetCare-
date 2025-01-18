from pydantic import BaseModel, Field
from typing import Annotated

class VetHistoryData(BaseModel):
    id: Annotated[str | None, Field(default=None, alias="_id")]
    date: Annotated[str, Field(max_length=10)]
    vet_name: Annotated[str, Field(max_length=30)]
    vet_phone_num: Annotated[str, Field(max_length=10)]
    health_level: Annotated[int, Field(ge=1, le=3)]
    summary: Annotated[str, Field(max_length=100)]
