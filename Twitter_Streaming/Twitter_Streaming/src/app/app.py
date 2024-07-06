
from flask import Flask, jsonify,request
from flask_restful import Api, Resource
from tweets_analyzer import Tweets_Analyser
from pymongo import MongoClient
import numpy as np
import pandas as pd
from flask_cors import CORS
import sys
import os

current_dir = os.path.dirname(__file__)
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

sys.path.append(parent_dir)


from config.config import config

app=Flask(__name__)
api=Api(app)
CORS(app)

def connect_to_db():
    try:
        client = MongoClient("mongodb://"+config['mongodb']['username']+":"+config['mongodb']['password']+"@localhost:27017/")
        db = client["Twitter_Tweets"]
        return db
    except Exception as e:
        print("Connection failed:", e)


def generate_response(data):
    with app.app_context():
            return jsonify(data)


class Tweets(Resource):

        
    def get(self,term):
        try:
            db=connect_to_db()
            tweets_cursor=db.Tweets.find({"text": {"$regex": term, "$options": "i"}})
            tweets_list=list(tweets_cursor)
            if not tweets_list:
                    result={"error":"Search term not found"}
                    return jsonify(result)
            analyzer=Tweets_Analyser(tweets_list)
            results = analyzer.query_term(term)
            results=generate_response(results)
            print(results.json)
            return results
        except Exception as e:
            error_response = {"error": "Internal Server Error"+e, "status_code": 500}
            return jsonify(error_response), 500
    
api.add_resource(Tweets,"/tweets/<string:term>")



if __name__=="__main__":
    app.run(debug=True)