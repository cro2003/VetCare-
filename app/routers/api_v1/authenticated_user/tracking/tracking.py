from fastapi import APIRouter, Header, Depends, HTTPException
from typing import Annotated
from app.dependencies import getAuthenticatedUser
from app.routers.api_v1.authenticated_user.tracking.models import DailyTrackingData
from app.dependencies import DbConnection
from bson.objectid import ObjectId
from app.dependencies import getPetData

tracking_router = APIRouter()

@tracking_router.post('/{pet_id}', status_code=201)
async def create_daily_tracking(user: Annotated[getAuthenticatedUser, Depends()], pet: Annotated[getPetData, Depends()], dailyTrackingData: DailyTrackingData, pet_collection: DbConnection):
    """
        Description:
        Create Daily Tracking Data

        Path

            - pet_id: Pet ID

        Header

            - authorization: token

        Request Body

            - datentime: Tracking Date & Time "2015-01-10 00:00:00"
            - weight: Weight of the Pet
            - diet: Diet Information of pet List of Dict
                    {"meal_type": "Lunch", datentime: "2015-01-10 00:00:00", "food": "Cereal", "amount": 809 [In grams] (Optional), "notes": "Good"(Optional)}
            - weight: Weight in KG
            - temperature: In Celsius
            - water_intake: In Litre(optional)
            - walking: In KMs(Optional)
            - Behaviour: Feeling Good
            - mood_indicator: 0 to 3 Rating
            - sleep_time: In Hours(Optional)
            - notes: Additional Notes
    """
    if pet.get('_id') not in user.get('pet_ids'):
        raise HTTPException(status_code=404, detail="Pet Not Found")

    dailyTrackingData.id = str(ObjectId())
    dailyTrackingData = dailyTrackingData.model_dump(by_alias=True)
    dailyTrackingData['pet_id'] = pet.get('_id')
    pet_collection.trackingCollection.insert_one(dailyTrackingData)
    return dailyTrackingData

@tracking_router.get('/{pet_id}')
async def get_daily_tracking(user: Annotated[getAuthenticatedUser, Depends()], pet: Annotated[getPetData, Depends()], pet_collection: DbConnection):
    """
        Description:
        Get Daily Tracking Data

        Path

            - pet_id: Pet ID

        Header

            - authorization: token
    """
    if pet.get('_id') not in user.get('pet_ids'):
        raise HTTPException(status_code=404, detail="Pet Not Found")

    data = pet_collection.trackingCollection.find({'pet_id': pet.get('_id')}).to_list()
    return {
        "daily_tracking": data
    }

@tracking_router.delete('/{pet_id}/{tracking_id}')
async def delete_daily_tracking(user: Annotated[getAuthenticatedUser, Depends()], pet: Annotated[getPetData, Depends()], tracking_id: str, pet_collection: DbConnection):
    """
        Description:
        Delete Daily Tracking Data

        Path

            - pet_id: Pet ID
            - tracking_id: Tracking ID

        Header

            - authorization: token
    """
    if pet.get('_id') not in user.get('pet_ids'):
        raise HTTPException(status_code=404, detail="Pet Not Found")

    pet_collection.trackingCollection.delete_one({'_id': tracking_id})
    return {
        "status": "Deleted"
    }

@tracking_router.get('/{pet_id}/{tracking_id}')
async def get_daily_tracking_by_id(user: Annotated[getAuthenticatedUser, Depends()], pet: Annotated[getPetData, Depends()], tracking_id: str, pet_collection: DbConnection):
    """
        Description:
        Get Daily Tracking Data by ID

        Path

            - pet_id: Pet ID
            - tracking_id: Tracking ID

        Header

            - authorization: token
    """
    if pet.get('_id') not in user.get('pet_ids'):
        raise HTTPException(status_code=404, detail="Pet Not Found")

    data = pet_collection.trackingCollection.find_one({'_id': tracking_id})
    return data
