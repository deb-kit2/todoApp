import json
from bson import ObjectId

from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient


class MongoJSONEncoder(json.JSONEncoder) :
    def default(self, o) :
        if isinstance(o, ObjectId) :
            return str(o)
        return json.JSONEncoder.default(self, o)


client = MongoClient("localhost", 27017)
db = client["admin"]

app = Flask(__name__)

@app.route("/")
def home() :
    tasks = list(db.myTodos.find({}))
    tasks = MongoJSONEncoder().encode(tasks)
    tasks = json.loads(tasks)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest" :
        return jsonify(tasks)
        
    return render_template("index.html")

if __name__ == "__main__" :
    app.run(debug = True)