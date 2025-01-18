from google import generativeai as genai
from app.config import Configs
from bson.objectid import ObjectId
from fastapi import HTTPException, status

genai.configure(api_key=Configs.GEMINI_API_KEY)

chats_object = {

}
class TextGeneration:
    def __init__(self, model=0, instruction="You are a Chatbot and can only help using Text Generation"):
        # instruction = "You are a Chatbot and can only help using Text Generation, "
        # "you have to strictly respond in json format without any text formatting for every chat"
        # "like {'result': 'YOUR_REPLY'}"
        self.models = {
            0: 'gemini-1.5-flash',
            1: 'gemini-1.5-pro',
            2: 'gemini-1.5-flash-8b',
            3: 'gemini-2.0-flash-exp'
        }
        self.model = genai.GenerativeModel(model_name=self.models[model], system_instruction=instruction)

    def start_chat(self, user_message):
        try:
            chat = self.model.start_chat()
            id = str(ObjectId())
            chats_object[id] = chat
            data = chat.send_message(user_message)
            return {'result': data.text, 'chatId': id}
        except Exception as e:
            return {'detail': e}

    def _check_chat(self, chatId):
        if not chats_object.get(chatId):
            return {'detail': 'Chat ID not Found'}

    def continue_chat(self, user_message, chatId):
        try:
            if self._check_chat(chatId):
                return self._check_chat(chatId)
            chat = chats_object[chatId]
            data = chat.send_message(user_message)
            return {'result': data.text}
        except Exception as e:
            return {'detail': e}

    def generate_text(self, user_message):
        try:
            data = self.model.generate_content(user_message)
            return {'result': data.text}
        except Exception as e:
            return {'detail': e}

class ImagetoTextGeneration():
    def __init__(self, model=0, instruction="You are a Chatbot and can only help using Text Generation"):
        # instruction = "You are a Chatbot and can only help using Text Generation, "
        # "you have to strictly respond in json format without any text formatting for every chat"
        # "like {'result': 'YOUR_REPLY'}"
        self.models = {
            0: 'gemini-1.5-flash',
            1: 'gemini-1.5-pro',
            2: 'gemini-1.5-flash-8b',
            3: 'gemini-2.0-flash-exp'
        }
        self.model = genai.GenerativeModel(model_name=self.models[model], system_instruction=instruction)