from datetime import datetime
import os
from flask import Flask, render_template, send_from_directory, request, Response, jsonify
from pymongo import MongoClient
import uniqid
import hashlib

class DropHandler:

    client = None
    clientHash = None
    
    def __init__(self, db):
        self.client = db.dead
        pass

    def get_timed_key(self):
        drop_id = uniqid.uniqid()
        self.client.formKeys.insert_one({"key": drop_id, "created": datetime.now()})
        return drop_id

    
    def stats(self):
        pipeline = [
            {"$sort": {"createdDate":-1}},
            {"$group": 
                { "_id": { "year":{"$year":"$createdDate"},"month":{"$month":"$createdDate"},"day":{"$dayOfMonth": "$createdDate"}},"count": { "$sum": 1 } } 
            },
            
        ]
        
        cursor = self.client.track.aggregate(pipeline)
        returnData =[]
        for document in cursor:
            dt = datetime(document['_id']['year'],document['_id']['month'],document['_id']['day'])
            returnData.append([int(dt.strftime('%s'))*1000,document['count']])
        
        def sort_by(a):
            return a[0]

        returnData= sorted(returnData, key=sort_by)

        return returnData

    def pickup(self, drop_id):
        cursor = self.client.drop.find({"key" :drop_id})
        tmp_data = []
        

        for document in cursor:
            tmp_data = document
            self.client.drop.remove({"key" :drop_id})
            self.client.track.update({"key" :drop_id},{"$set":{"pickedUp":datetime.now()},"$unset":{"key":""}})
            break

        if tmp_data:

            #handle old drops without createdDate
            if "createdDate" in tmp_data:
                # Do not return drops > 24 hours old
                time_delta = datetime.now()  - tmp_data["createdDate"]

                if time_delta.days > 1:
                    print("too old, retunring None")
                    return []

            return tmp_data["data"]

        return []

    def drop(self, data):
        key = uniqid.uniqid()
        self.client.drop.insert_one({"key" :key, "data":data, "createdDate":datetime.now()})
        self.client.track.insert_one({"key" :key, "userHash": self.clientHash, "createdDate":datetime.now(),"pickedUp":None})
        return key

    def setRequestHash(self,ipAddr):
        m = hashlib.sha256()
        m.update(ipAddr.encode('utf-8'))
        self.clientHash = m.hexdigest()


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
    return jsonify(key)


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
