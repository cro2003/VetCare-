from fastapi import APIRouter, Header, Depends, HTTPException
from typing import Annotated
from app.dependencies import getAuthenticatedUser
from app.routers.api_v1.authenticated_user.reminder.models import ReminderData
from app.dependencies import DbConnection
from bson.objectid import ObjectId
from app.dependencies import getPetData

reminder_router = APIRouter()

@reminder_router.post('/{pet_id}')
async def create_reminder(user: Annotated[getAuthenticatedUser, Depends()], pet: Annotated[getPetData, Depends()], reminderData: ReminderData, pet_collection: DbConnection):
    """
        Description:
        Create Reminder for Pet

        Header

            - authorization: token

        Request Body

            - date: Date of Task
            - summary : Summary or Notes
            - severity: Rating 1 to 3
    """
    if pet.get('_id') not in user.get('pet_ids'):
        raise HTTPException(status_code=404, detail="Pet Not Found")

    reminderData.id = str(ObjectId())
    reminderData = reminderData.model_dump(by_alias=True)
    reminderData['pet_id'] = pet.get('_id')
    reminderData['user_id'] = user.get('_id')

    pet_collection.remindersCollection.insert_one(reminderData)
    return reminderData

@reminder_router.get('/')
async def get_reminders(user: Annotated[getAuthenticatedUser, Depends()], pet_collection: DbConnection):
    """
        Description:
        Get Reminders of all Pets

        Header

            - authorization: token
    """
    reminders = pet_collection.remindersCollection.find({'user_id': user.get('_id')}).to_list()
    return {'reminders': reminders}