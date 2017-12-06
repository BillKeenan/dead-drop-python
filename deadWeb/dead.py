from flask import Flask, render_template, send_from_directory, request
from jinja2 import Template
from flask import jsonify
from pymongo import MongoClient
import uuid
from datetime import datetime

import os
app = Flask(__name__)

@app.route("/")
def index():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    return render_template('index.htm',timedKey=get_timed_key())

@app.route('/images/<path:path>')
def send_images(path):
    return send_from_directory('images', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route("/drop",methods = ['POST'])
def drop():





    #ok, looks alright
    data = request.form["data"];
    key = request.form["key"];

# //data should look as expected, and parse as data
# $jsonData = json_decode($data);

# $keysToCheck = ["iv","v","iter","ks","ts","mode","adata","cipher","salt","ct"];

# //verify our various keys
# foreach($keysToCheck as $key=>$value){
#     if (! property_exists($jsonData,$value)){
#         header('HTTP/1.1 500 Internal Server Error');
#         print("data missing:".$value);
#         exit;
#     }
# }



    client = MongoClient()
    db = client.dead
    db.drop.insert_one({ "key" :key, "data":data})
    return jsonify(id=1234)

@app.route("/pickup/<id>")
def pickupDrop(id):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    return render_template('index.htm',id=id)



if __name__ == "__main__":
    app.run(host='0.0.0.0')


def get_timed_key():
    id = uuid.uuid4();
    client = MongoClient()
    db = client.dead
    db.formKeys.insert_one({"key": id,"created": datetime.now()})
    return id
