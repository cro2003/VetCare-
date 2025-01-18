from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, List, Optional
from app.routers.api_v1.auth.models import PersonalVetInfo
class UpdateUserData(BaseModel):
    full_name: str | None =  Field(max_length=30, default=None)
    email: EmailStr | None =  Field(default=None)
    phone_num: str | None = Field(max_length=10, default=None)
    address: str | None = Field(max_length=100, default=None)
    vet_info: Optional[PersonalVetInfo] = Field(default=None)
    pet_ids: Optional[List[str]] = Field(default=None)
    reminder_ids: Optional[List[str]] = Field(default=None)