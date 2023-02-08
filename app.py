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
    del user_input["_id"]

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
    
@app.route("/delete", methods = ["DELETE"])
def deleteTask() :
    user_input = request.get_json()
    user_input["_id"] = ObjectId(user_input["_id"])

    db.myTodos.delete_one(user_input)

    return jsonify({"result": "Ok"}), 200

@app.route("/edit", methods = ["PUT"])
def editTask() :
    user_input = request.get_json()
    user_input["_id"] = ObjectId(user_input["_id"])

    db.myTodos.update_one(
        {"_id" : user_input["_id"]}, 
        {"$set" : {
            "title" : '\u0336'.join(user_input["title"]) + '\u0336',
            "description" : '\u0336'.join(user_input["description"]) + '\u0336',
            "status" : "complete"
        }}
    )

    return jsonify({"result": "Ok"}), 200


if __name__ == "__main__" :
    app.run(debug = True)