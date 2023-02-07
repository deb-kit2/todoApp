import json
from bson import ObjectId

from pymongo import MongoClient


class MongoJSONEncoder(json.JSONEncoder) :
    def default(self, o) :
        if isinstance(o, ObjectId) :
            return str(o)
        return json.JSONEncoder.default(self, o)


client = MongoClient("localhost", 27017)
db = client["admin"]

tasks = list(db.myTodos.find({}))