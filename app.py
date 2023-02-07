from flask import Flask, render_template
from flask import jsonify

from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.

app = Flask(__name__)

@app.route("/")
def home() :
    return render_template("index.html")

if __name__ == "__main__" :
    app.run(debug = True)