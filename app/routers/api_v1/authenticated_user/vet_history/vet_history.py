from fastapi import APIRouter, Header, Depends, HTTPException
from typing import Annotated
from app.dependencies import getAuthenticatedUser
from app.routers.api_v1.authenticated_user.vet_history.models import VetHistoryData
from app.dependencies import DbConnection
from bson.objectid import ObjectId
from app.dependencies import getPetData

vet_history_router = APIRouter()

@vet_history_router.post('/{pet_id}', status_code=201)
async def create_vet_history(user: Annotated[getAuthenticatedUser, Depends()], pet: Annotated[getPetData, Depends()], vetHistoryData: VetHistoryData, pet_collection: DbConnection):
    """
        Description:
        Store Vet Visit history of Pet

        Header

            - authorization: token

        Request Body

            - pet_id: Pet ID
            - vet_name: Vet Name
            - vet_phone_num: Phone number of Vet
            - reason: Reason of Visit
            - health_level: Health Level of Pet Out of 3
            - summary: Comments by Doctor
    """
    if pet.get('_id') not in user.get('pet_ids'):
        raise HTTPException(status_code=404, detail="Pet Not Found")

    vetHistoryData.id = str(ObjectId())
    vetHistoryData = vetHistoryData.model_dump(by_alias=True)
    vetHistoryData['pet_id'] = pet.get('_id')

    pet_collection.vet_historyCollection.insert_one(vetHistoryData)
    return vetHistoryData

@vet_history_router.get('/{pet_id}')
async def get_vet_history(user: Annotated[getAuthenticatedUser, Depends()], pet: Annotated[getPetData, Depends()], pet_collection: DbConnection):
    """
        Description:
        Get Vet Visit history of Pet

        Header

            - authorization: token
    """
    if pet.get('_id') not in user.get('pet_ids'):
        raise HTTPException(status_code=404, detail="Pet Not Found")

    vet_history = pet_collection.vet_historyCollection.find({'pet_id': pet.get('_id')}).to_list()
    return vet_history

@vet_history_router.get('/{pet_id}/{vet_id}')
async def get_vet_history_by_id(user: Annotated[getAuthenticatedUser, Depends()], pet: Annotated[getPetData, Depends()], vet_id: str, pet_collection: DbConnection):
    """
        Description:
        Get Vet Visit history of Pet by ID

        Header

            - authorization: token
    """
    if pet.get('_id') not in user.get('pet_ids'):
        raise HTTPException(status_code=404, detail="Pet Not Found")

    vet_history = pet_collection.vet_historyCollection.find_one({'_id': vet_id})
    return {'vet_histories': vet_history}

@vet_history_router.delete('/{pet_id}/{vet_id}')
async def delete_vet_history(user: Annotated[getAuthenticatedUser, Depends()], pet: Annotated[getPetData, Depends()], vet_id: str, pet_collection: DbConnection):
    """
        Description:
        Delete Vet Visit history of Pet

        Header

            - authorization: token
    """
    if pet.get('_id') not in user.get('pet_ids'):
        raise HTTPException(status_code=404, detail="Pet Not Found")

    pet_collection.vet_historyCollection.delete_one({'_id': vet_id})
    return {
        "success": "True"
   }