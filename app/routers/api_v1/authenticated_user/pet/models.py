from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, List, Optional
from app.routers.api_v1.auth.models import PersonalVetInfo
from datetime import datetime

class Disease(BaseModel):
    name: str
    date: str

class Vaccine(BaseModel):
    name: str
    date: str

class Medication(BaseModel):
    name: str
    date: str

class Allergies(BaseModel):
    name: str
    date: str

class PetData(BaseModel):
    id: Annotated[str | None, Field(default=None, alias="_id")]
    name: Annotated[str, Field(max_length=30)]
    breed: Annotated[str, Field(max_length=30)]
    dob: str
    weight: Annotated[float, Field(ge=1)]
    gender: Annotated[str, Field(max_length=1)]
    reproduction: bool
    pregnancy: bool
    allergies: Optional[List[Allergies]] = Field(default=[])
    diseases: Optional[List[Disease]] = Field(default=[])
    vaccine: Optional[List[Vaccine]] = Field(default=[])
    medication: Optional[List[Medication]] = Field(default=[])

class UpdatePetdata(BaseModel):
    id: Annotated[Optional[str], Field(default=None, alias="_id")]
    name: Annotated[Optional[str], Field(default=None, max_length=30)]
    breed: Annotated[Optional[str], Field(default=None, max_length=30)]
    dob: Annotated[Optional[str], Field(default=None)]
    weight: Annotated[Optional[float], Field(default=None, ge=1)]
    gender: Annotated[Optional[str], Field(default=None, max_length=1)]
    reproduction: Optional[bool] = None
    pregnancy: Optional[bool] = None
    allergies: Optional[List["Allergies"]] = Field(default=None)
    diseases: Optional[List["Disease"]] = Field(default=None)
    vaccine: Optional[List["Vaccine"]] = Field(default=None)
    medication: Optional[List["Medication"]] = Field(default=None)