from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.database import MongoConnection
from fastapi import Header, Body, Path
from app.authentication import Autheticate

DbConnection = Annotated[MongoConnection, Depends()]

def getUserData(user_num: str, user_collection: DbConnection):
    if user_num.isnumeric():
        user_num = int(user_num)
    user = user_collection.UsersCollection.find_one({
        '$or': [
            {'user_num': user_num},
            {'email': user_num}
        ]
    })
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

def getUserDataId(user_id: str, user_collection: DbConnection):
    user = user_collection.UsersCollection.find_one({'_id': user_id})
    if user:
        return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")

def getAuthenticatedUser(authorization: Annotated[str, Header()]):
    a = Autheticate()
    user_id = a.verify_user(authorization)
    if user_id:
        return getUserDataId(user_id, DbConnection())
    raise HTTPException(status_code=498, detail="Invalid Token")

def getPetData(pet_id: Annotated[str, Path()], pet_collection: DbConnection):
    pet = pet_collection.petsCollection.find_one({'_id': pet_id})
    pet.get('dob')
    if pet:
        return pet
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet Not Found")