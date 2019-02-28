# -*- coding: utf-8 -*-
from flask import Flask
from core.db_mongo import MyMongo

app = Flask(__name__)
my_mongo = MyMongo()
my_mongo.connect()

@app.route('/')
def index():
    try:
        proxy = my_mongo.find(True)
        my_mongo.close()
        return "<h2>{}:{}</h2><b>{}<b>".format(proxy['ip'],proxy['port'],proxy['addr'])
    except:
        return "等等再刷新.."


def start_server():
    app.run(host='0.0.0.0')