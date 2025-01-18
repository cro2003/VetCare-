from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional, List

class PersonalVetInfo(BaseModel):
    full_name: Annotated[str, Field(max_length=30)]
    phone_num: Annotated[str, Field(max_length=10)]

class UserData(BaseModel):
    id: Annotated[str | None, Field(default=None, alias="_id")]
    user_num: Annotated[int | None, Field(default="")]
    full_name: Annotated[str, Field(max_length=30)]
    role: Annotated[str | None, Field(default='user', exclude=True)]
    email: EmailStr
    phone_num: Annotated[str, Field(max_length=10)]
    address: Annotated[str, Field(max_length=100)]
    vet_info: PersonalVetInfo
    pet_ids: Optional[List[str]] = Field(default=None)
    reminder_ids: Optional[List[str]] = Field(default=None)

class UserwithPass(UserData):
    password: str