from pydantic import BaseModel, Field
from typing import Annotated, List, Optional

class Meal(BaseModel):
    meal_type: Annotated[str, Field(max_length=30, description="Meal Type like Breakfast, Lunch, Dinner")]
    datentime: Annotated[str, Field(max_length=30, description="Date and Time")]
    food: Annotated[str, Field(max_length=30, description="Food Name")]
    amount: Optional[int] = Field(description="Amount in grams", default=None)
    notes: Optional[str] = Field(description="Notes", default="")

class DailyTrackingData(BaseModel):
    id: Annotated[str | None, Field(default=None, alias="_id")]
    datentime: Annotated[str, Field(max_length=30, description="Date and Time")]
    diet: Optional[List[Meal]] = Field(description="List of Meal", default=[])
    weight: Annotated[float, Field(ge=0, description="Weight in KG")]
    temperature: Annotated[float, Field(ge=1, description="Temperature in Celsius")]
    water_intake: Optional[float] = Field(ge=0, description="Water Intake in litre", default=None)
    walking: Optional[float] = Field(ge=0, description="Walking in KM", default=None)
    behavior: Annotated[str, Field(max_length=100, description="Behavior of the Pet")]
    mood_indicator: Annotated[int, Field(ge=1, le=3, description="Mood Indicator from 3")]
    sleep_time: Optional[float] = Field(ge=0, description="Sleeping Time in Hour", default=None)
    notes: Annotated[str, Field(max_length=500, description="Notes")]