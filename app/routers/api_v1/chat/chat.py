from fastapi import APIRouter, Path, Body, Depends
from app.gemini import TextGeneration
from app.routers.api_v1.chat.models import ChatMessage, TextMessages
from typing import Annotated
from app.dependencies import DbConnection

chat_router = APIRouter()

def get_pet_info(pet_id, collections: Annotated[DbConnection, Depends()]):
    pet_info = collections.petsCollection.find_one({'_id': pet_id})
    daily_info = collections.trackingCollection.find({'_id': pet_id})[:7]
    return {
        "pet_info": pet_info,
        "daily_info": daily_info
    }



@chat_router.post('/')
async def chat_start(chatMessage: Annotated[ChatMessage, Body()], pet_info: Annotated[get_pet_info, Depends()]):
    """
        Description
        Create a New Chat & responds with Chat Response & chatId

        Request Body

            - message: User Message
    """
    t = TextGeneration(instruction=pet_info)
    return t.start_chat(chatMessage.message)

@chat_router.post('/{chat_id}')
async def continue_chat(chat_id: Annotated[str, Path()], chatMessage: Annotated[ChatMessage, Body()]):
    """
        Description
        Resume the Existing Chat & Responds according to previous Chat

        Path Parameter

            - chatId: Chat Id which was received after Starting the Chat

        Request Body

            - message: User Message
    """
    t = TextGeneration()
    return t.continue_chat(chatId=chat_id, user_message=chatMessage.message)

# @chat_router.post('/text')
# async def text_generation(textMessage: Annotated[TextMessages, Body()]):
#     t = TextGeneration()
#     return t.generate_text(textMessage.message)

