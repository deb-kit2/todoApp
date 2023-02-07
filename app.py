import json
from bson import ObjectId

from flask import Flask, render_template, jsonify, request, redirect, url_for
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
def index() :
    tasks = list(db.myTodos.find({}))
    tasks = MongoJSONEncoder().encode(tasks)
    tasks = json.loads(tasks)

    if request.headers.get("X-Requested-With") == "XMLHttpRequest" :
        return jsonify(tasks)

    return render_template("index.html")

@app.route("/create", methods = ["POST"])
def createTask() :
    user_input = request.get_json()

    # validation, add checks
    if len(user_input["title"]) < 1 :  
        print("Could not add! Bad entry! :(")
    else :
        db.myTodos.insert_one(user_input)
        
        # safe return
        t = MongoJSONEncoder().encode(user_input)
        t = json.loads(t)
        return jsonify(t)

    return redirect(url_for("index"))
    
    

if __name__ == "__main__" :
    app.run(debug = True)