from fastapi import APIRouter, Header, Depends
from typing import Annotated
from app.dependencies import getAuthenticatedUser
from app.routers.api_v1.authenticated_user.models import UpdateUserData
from app.dependencies import DbConnection
from app.routers.api_v1.authenticated_user.pet import pet_router
from app.routers.api_v1.authenticated_user.tracking import tracking_router
from app.routers.api_v1.authenticated_user.vet_history import vet_history_router

authenticated_user_router = APIRouter()
authenticated_user_router.include_router(pet_router, prefix='/pet', tags=['pet'])
authenticated_user_router.include_router(tracking_router, prefix='/tracking', tags=['tracking'])
authenticated_user_router.include_router(vet_history_router, prefix='/vet_history', tags=['vet_history'])

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