from fastapi import APIRouter, Header, Depends
from typing import Annotated
from app.dependencies import getAuthenticatedUser
from app.routers.api_v1.authenticated_user.models import UpdateUserData
from app.dependencies import DbConnection
from app.routers.api_v1.authenticated_user.pet import pet_router
from app.routers.api_v1.authenticated_user.tracking import tracking_router
from app.routers.api_v1.authenticated_user.vet_history import vet_history_router
from app.routers.api_v1.authenticated_user.reminder import reminder_router
from datetime import datetime

authenticated_user_router = APIRouter()
authenticated_user_router.include_router(pet_router, prefix='/pet', tags=['pet'])
authenticated_user_router.include_router(tracking_router, prefix='/tracking', tags=['tracking'])
authenticated_user_router.include_router(vet_history_router, prefix='/vet_history', tags=['vet_history'])
authenticated_user_router.include_router(reminder_router, prefix='/reminder', tags=['reminder'])

@authenticated_user_router.get('/profile')
async def profile(user: Annotated[getAuthenticatedUser, Depends()]):
    """
        Description:
        Show User Info

        Header

            - authorization: token
    """
    return user

@authenticated_user_router.put('/profile')
async def update_profile(user: Annotated[getAuthenticatedUser, Depends()], userData: UpdateUserData, user_collection: DbConnection):
    """
        Description:
        Update User Info

        Header

            - authorization: token

        Request Body

                - full_name: User Full Name
                - email: email address
                - phone_num: Phone Number
                - address: Address
                - vet_info: Personal Vet Info
                - pet_ids: List of Pet IDs
                - reminder_ids: List of Reminder IDs
    """
    updated_data = userData.model_dump(exclude_unset=True)
    if updated_data=={}:
        return user
    user_collection.UsersCollection.update_one(
        {'_id': user.get('_id')},
        {'$set': updated_data}
    )
    return user_collection.UsersCollection.find_one({'_id': user.get('_id')})

@authenticated_user_router.get('/notification')
async def get_notifications(user: Annotated[getAuthenticatedUser, Depends()], reminder_collection: DbConnection):
    """
        Description:
        Get Notifications

        Header

            - authorization: token
    """
    reminders = reminder_collection.remindersCollection.find({'user_id': user.get('_id')}).to_list()
    notifications = []
    for reminder in reminders:
        if reminder.get('date')[:10] == str(datetime.now().date()):
            notifications.append(reminder)
    return {'notifications': notifications}

@authenticated_user_router.get('/calender')
async def get_calender(user: Annotated[getAuthenticatedUser, Depends()], reminder_collection: DbConnection):
    """
        Description:
        Get Calender

        Header

            - authorization: token
    """
    reminders = reminder_collection.remindersCollection.find({'user_id': user.get('_id')}).to_list()
    calender = {}
    for reminder in reminders:
        calender[reminder.get('date')] = reminder
    return {'calender': calender}