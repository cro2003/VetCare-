import os
from dotenv import load_dotenv

load_dotenv()

class Configs():
    MONGO_DB_URL = os.getenv('MONGO_DB_URL')
    CURRENT_DB = os.getenv('CURRENT_DB')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')