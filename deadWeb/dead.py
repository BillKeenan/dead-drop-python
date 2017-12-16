from flask import Flask, render_template, send_from_directory, request, Response 
from jinja2 import Template
from flask import jsonify
from pymongo import MongoClient
import uniqid
from datetime import datetime
from pprint import pprint
import os


class drop_handler:

  client = None

  def __init__(self, db):
    self.client = db.dead
    pass

  def get_timed_key(self):
      id = uniqid.uniqid()
      
      self.client.formKeys.insert_one({"key": id,"created": datetime.now()})
      return id

  def pickup(self,id):
    cursor = self.client.drop.find({ "key" :id})
    tmpData = []
    for document in cursor:
      tmpData = document
      cursor = self.client.drop.remove({ "key" :id})
      break
    
    if (tmpData):

        #handle old drops without createdDate
        if "createdDate" in tmpData:
            # Do not return drops > 24 hours old
            timeDelta = datetime.now()  - tmpData["createdDate"]

            if timeDelta.days > 1 :
                print("too old, retunring None")
                return []

        return tmpData["data"]

    return []

  def drop(self,data):
    key = uniqid.uniqid()
    self.client.drop.insert_one({ "key" :key, "data":data,"createdDate":datetime.now()})
    return key



handler = drop_handler(MongoClient())

app = Flask(__name__)

@app.route("/")
def index():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    return render_template('index.htm',timedKey= handler.get_timed_key())

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
    key = handler.drop(request.form["data"])
    return jsonify(id=key)

@app.route("/pickup/<id>")
def pickupDropIndex(id):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    return render_template('index.htm',id=id)


@app.route("/getdrop.php?id=<id>")
@app.route("/drop/<id>")
def picupDropJSON(id):
  returnData = handler.pickup(id)
  return  Response(returnData,mimetype='application/json')



if __name__ == "__main__":
    app.run(host='0.0.0.0')

