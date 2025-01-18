from fastapi import APIRouter, Header, Depends, HTTPException
from typing import Annotated
from app.dependencies import getAuthenticatedUser
from app.routers.api_v1.authenticated_user.pet.models import PetData, UpdatePetdata
from app.dependencies import DbConnection
from bson.objectid import ObjectId
from datetime import datetime
from app.dependencies import getPetData

pet_router = APIRouter()

@pet_router.post('/', status_code=201)
async def create_pet(user: Annotated[getAuthenticatedUser, Depends()], petData: PetData, pet_collection: DbConnection):
    """
        Description:
        Onboard Pet

        Header

            - authorization: token

        Request Body

            - name: name of the Pet
            - breed: Pet Breed
            - dob: Birth Date of Pet [DD/MM/YYYY]
            - weight: weight of the Pet
            - gender: Gender of the Pet
            - reproduction: Reproduction Status
            - pregnancy: Pregnancy Status
            - allergies: List of Dict {"name: str, date: str [DD/MM/YYYY]"}
            - diseases: List of Dict {"name: str, date: str [DD/MM/YYYY]"}
            - vaccine: List of Dict {"name: str, date: str [DD/MM/YYYY]"}
            - medication: List of Dict {"name: str, date: str [DD/MM/YYYY]"}
    """
    petData.id = str(ObjectId())
    petData = petData.model_dump(by_alias=True)

    """ Date Handling Start"""
    date_object = datetime.strptime(petData['dob'], "%d/%m/%Y")
    petData['dob'] = str(date_object)
    for num in range(len(petData['allergies'])):
        date_object = datetime.strptime(petData['allergies'][num]['date'], "%d/%m/%Y")
        petData['allergies'][num]['date'] = str(date_object)
    for num in range(len(petData['diseases'])):
        date_object = datetime.strptime(petData['diseases'][num]['date'], "%d/%m/%Y")
        petData['diseases'][num]['date'] = str(date_object)
    for num in range(len(petData['vaccine'])):
        date_object = datetime.strptime(petData['vaccine'][num]['date'], "%d/%m/%Y")
        petData['vaccine'][num]['date'] = str(date_object)
    for num in range(len(petData['medication'])):
        date_object = datetime.strptime(petData['medication'][num]['date'], "%d/%m/%Y")
        petData['medication'][num]['date'] = str(date_object)
    """ Date Handling End"""

    pet_collection.petsCollection.insert_one(petData)
    pet_collection.UsersCollection.update_one(
        {'_id': user.get('_id')},
        {'$push': {'pet_ids': petData.get('_id')}}
    )
    return petData

@pet_router.get('/{pet_id}', response_model=PetData)
async def get_pet(user: Annotated[getAuthenticatedUser, Depends()], pet: Annotated[getPetData, Depends()]):
    """
        Description:
        Get Pet Info

        Path

            - pet_id: Pet ID
    """
    if pet.get('_id') not in user.get('pet_ids'):
        raise HTTPException(status_code=404, detail="Pet Not Found")
    return pet

@pet_router.put('/{pet_id}', response_model=PetData)
async def update_pet(user: Annotated[getAuthenticatedUser, Depends()], pet: Annotated[getPetData, Depends()], petData: UpdatePetdata, pet_collection: DbConnection):
    """
        Description:
        Update Pet Info

        Path

            - pet_id: Pet ID

        Request Body

            - name: name of the Pet
            - breed: Pet Breed
            - dob: Birth Date of Pet [DD/MM/YYYY]
            - weight: weight of the Pet
            - gender: Gender of the Pet
            - reproduction: Reproduction Status
            - pregnancy: Pregnancy Status
            - allergies: List of Dict {"name: str, date: str [DD/MM/YYYY]"}
            - diseases: List of Dict {"name: str, date: str [DD/MM/YYYY]"}
            - vaccine: List of Dict {"name: str, date: str [DD/MM/YYYY]"}
            - medication: List of Dict {"name: str, date: str [DD/MM/YYYY]"}
    """
    if pet.get('_id') not in user.get('pet_ids'):
        raise HTTPException(status_code=404, detail="Pet Not Found")
    updated_data = petData.model_dump(exclude_unset=True)
    if updated_data=={}:
        return pet_collection.petsCollection.find_one({'_id': pet.get('_id')})

    """ Date Handling Start"""
    if 'dob' in updated_data:
        date_object = datetime.strptime(petData['dob'], "%d/%m/%Y")
        petData['dob'] = str(date_object)
    if 'allergies' in updated_data:
        for num in range(len(petData['allergies'])):
            date_object = datetime.strptime(petData['allergies'][num]['date'], "%d/%m/%Y")
            petData['allergies'][num]['date'] = str(date_object)
    if 'diseases' in updated_data:
        for num in range(len(petData['diseases'])):
            date_object = datetime.strptime(petData['diseases'][num]['date'], "%d/%m/%Y")
            petData['diseases'][num]['date'] = str(date_object)
    if 'vaccine' in updated_data:
        for num in range(len(petData['vaccine'])):
            date_object = datetime.strptime(petData['vaccine'][num]['date'], "%d/%m/%Y")
            petData['vaccine'][num]['date'] = str(date_object)
    if 'medication' in updated_data:
        for num in range(len(petData['medication'])):
            date_object = datetime.strptime(petData['medication'][num]['date'], "%d/%m/%Y")
            petData['medication'][num]['date'] = str(date_object)
    """ Date Handling End"""

    pet_collection.petsCollection.update_one(
        {'_id': pet.get('_id')},
        {'$set': updated_data}
    )
    return pet_collection.petsCollection.find_one({'_id': pet.get('_id')})

@pet_router.delete('/{pet_id}', response_model=PetData)
async def delete_pet(user: Annotated[getAuthenticatedUser, Depends()], pet: Annotated[getPetData, Depends()], pet_collection: DbConnection):
    """
        Description:
        Delete Pet

        Path

            - pet_id: Pet ID
    """
    if pet.get('_id') not in user.get('pet_ids'):
        raise HTTPException(status_code=404, detail="Pet Not Found")
    pet_collection.UsersCollection.update_one(
        {'_id': user.get('_id')},
        {'$pull': {'pet_ids': pet.get('_id')}}
    )
    return pet