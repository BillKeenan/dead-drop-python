from datetime import datetime
import os
from flask import Flask, render_template, send_from_directory, request, Response, jsonify
from pymongo import MongoClient
import uniqid
import hashlib
import json

class DropHandler:

    client = None
    clientHash = None
    salt = "a6891cca-3ea1-4f56-b3a8-1d77095a088e"
    
    def __init__(self, db):
        self.client = db.dead
        pass

    def get_timed_key(self):
        drop_id = uniqid.uniqid()
        self.client.formKeys.insert_one({"key": drop_id, "created": datetime.now()})
        return drop_id

    
    def stats(self):
        pipeline = [
            {"$group": 
            { "_id": { "year":{"$year":"$createdDate"},"month":{"$month":"$createdDate"},"day":{"$dayOfMonth": "$createdDate"},"userHash":"$userHash"},
                "count": { "$sum": 1 },
            }
            },
            {"$group":
                { "_id": { "year":"$_id.year","month":"$_id.month","day":"$_id.day"},
                "count": { "$sum": "$count" },
                "distinctCount": { "$sum": 1 }
                }
            },
            {"$sort":  {"_id.year":1,"_id.month":1,"_id.day":1}},

        ]

        cursor = self.client.track.aggregate(pipeline)
        returnData =[]
        countData=[]
        uniqueData=[]
        for document in cursor:
            if (document['_id'] == "1"):
                continue
            dt = datetime(document['_id']['year'],document['_id']['month'],document['_id']['day'])
            countData.append([int(dt.strftime('%s'))*1000,document['count'],])
            uniqueData.append([int(dt.strftime('%s'))*1000,document['distinctCount']])
        
        def sort_by(a):
             return a[0]
 	 
        countData= sorted(countData, key=sort_by)
        uniqueData= sorted(uniqueData, key=sort_by)

        returnData.append({"label":"# of Drops","data":countData})
        returnData.append({"label":"Unique Users","data":uniqueData})

        return returnData

    def pickup(self, drop_id):
        document = self.client.drop.find_one_and_delete({"key" :drop_id})

        if (document == []):
            return []
        
        self.client.track.update({"key" :drop_id},{"$set":{"pickedUp":datetime.now()},"$unset":{"key":""}})

        #handle old drops without createdDate
        if "createdDate" in document:
            # Do not return drops > 24 hours old
            time_delta = datetime.now()  - document["createdDate"]

            if time_delta.days > 1:
                # "too old, returning None"
                return []
            else:
                return document["data"]
        else:
            # no create date, no drop for you
            return []


    def drop(self, data):
        key = uniqid.uniqid()
        self.client.drop.insert_one({"key" :key, "data":data, "createdDate":datetime.now()})
        self.client.track.insert_one({"key" :key, "userHash": self.clientHash, "createdDate":datetime.now(),"pickedUp":None})
        return key

    def setRequestHash(self,ipAddr):
        # dont want people using a rainbow table to look up these ip's
        saltedIP = self.salt +ipAddr
        m = hashlib.sha256()
        m.update(saltedIP.encode('utf-8'))
        self.clientHash = m.hexdigest()[:32]


HANDLER = DropHandler(MongoClient())


APP = Flask(__name__)

@APP.route("/")
def index():
    """ just return the index template"""
    return render_template('index.htm', timedKey=HANDLER.get_timed_key())

@APP.route("/stats")
def statsindex():
    """ just return the stats"""
    return render_template('stats.htm', timedKey=HANDLER.get_timed_key())


@APP.route("/stats/json")
def statsjson():

    """ just return the stats"""
    key = HANDLER.stats()
    return Response(json.dumps(key, indent=4, sort_keys=True), mimetype='application/json')


@APP.route('/images/<path:path>')
def send_images(path):
    """load images from drive path"""
    return send_from_directory('images', path)

@APP.route('/js/<path:path>')
def send_js(path):
    """load js from drive path"""
    return send_from_directory('js', path)

@APP.route('/css/<path:path>')
def send_css(path):
    """load css from drive path"""
    return send_from_directory('css', path)


@APP.route("/drop", methods = ['POST'])
def drop():
    """ok, looks alright"""
    HANDLER.setRequestHash(request.remote_addr)
    key = HANDLER.drop(request.form["data"])
    return jsonify(id=key)

@APP.route("/pickup/<drop_id>")
def pickup_drop_index(drop_id):
    """Load the pickup HTML"""
    return render_template('index.htm', id=drop_id)


@APP.route("/getdrop.php?id=<drop_id>")
@APP.route("/drop/<drop_id>")
def pickup_drop_json(drop_id):
    """Actually get the drop from the DB"""
    return_data = HANDLER.pickup(drop_id)
    return  Response(return_data, mimetype='application/json')
