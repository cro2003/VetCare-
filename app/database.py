from app.config import Configs
from pymongo import MongoClient

class MongoConnection():
    def __init__(self):
        self.client = MongoClient(Configs.MONGO_DB_URL)
        self.db = self.client[Configs.CURRENT_DB]
        self.initialize()

    def initialize(self):
        self.UsersCollection = self.db['users']
        self.TokensCollection = self.db['tokens']
        self.petsCollection = self.db['pets']
        self.trackingCollection = self.db['trackers']
        self.vet_historyCollection = self.db['vet_history']
        self.remindersCollection = self.db['reminders']