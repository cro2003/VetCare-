from bson.objectid import ObjectId
from hashlib import sha256
from app.database import MongoConnection

class Autheticate():
    def __init__(self):
        self.DbConection = MongoConnection()

    def _hash_generator(self, string):
        obj = sha256(string.encode())
        return obj.hexdigest()

    def create_token(self, id):
        token = self._hash_generator(str(ObjectId()))
        self.DbConection.TokensCollection.insert_one(
            {
                "_id": token,
                "value": id
            }
        )
        return token

    def verify_user(self, token):
        data = self.DbConection.TokensCollection.find_one({
            "_id": token
        })
        if data:
            return data['value']
        return None

    def delete_token(self, token):
        self.DbConection.TokensCollection.delete_one({
            "_id": token
        })