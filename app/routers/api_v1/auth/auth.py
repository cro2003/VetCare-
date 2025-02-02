from fastapi import Response, APIRouter, Body, HTTPException, status, Header
from app.authentication import Autheticate
from app.dependencies import DbConnection, getUserData
from app.routers.api_v1.auth.models import UserwithPass
from bson.objectid import ObjectId
from typing import Annotated

auth_route = APIRouter()
@auth_route.post('/signup', status_code=201)
async def signup(user: UserwithPass, user_collection: DbConnection, response: Response):
    """
        Description:
        Signup Into the System

        Request Body

            - full_name: User Full Name
            - email: email address
            - password: hash
            - phone_num: Phone Number
            -address: Address
            - vet_info: Vet Information
    """
    current_num = user_collection.UsersCollection.find_one({'_id': '67875d97a783e495e31d4b91'}).get('currentNum')
    user.id = str(ObjectId())
    user.user_num = current_num + 1
    user_collection.UsersCollection.insert_one(user.model_dump(by_alias=True))
    user_collection.UsersCollection.update_one({'_id': '67875d97a783e495e31d4b91'},
                                               {'$set': {'currentNum': current_num + 1}})
    a = Autheticate()
    token = a.create_token(user.id)
    response.headers['authorization'] = token
    data = user.model_dump()
    data.update({'token': token})
    return data

@auth_route.post('/login')
async def login(username: Annotated[str, Body()], password: Annotated[str, Body()], response: Response):
    """
    Description:
    Login Into the System

    Request Body

        - username: email address
        - password: hash
    """
    user = getUserData(username, DbConnection())
    if not (user['password'] == password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Password")
    a = Autheticate()
    token = a.create_token(user['_id'])
    response.headers['authorization'] = token
    return {'token': token}

@auth_route.get('/logout')
async def logout(authorization: Annotated[str, Header()]):
    """
        Description:
        Logout From the System

        Header

            - authorization: token
    """
    a = Autheticate()
    a.delete_token(authorization)
    return {'success': True}