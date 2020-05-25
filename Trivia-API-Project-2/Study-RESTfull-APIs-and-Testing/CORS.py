from flask import Flask , jsonify
from flask_cors import CORS, cross_origin
import unittest
from unittest import TestCase
app  = Flask(__name__)



@app.route('/api/posts')
# because of that decorator any cors origin request will be accepted 
@cross_origin()
def getPosts():
    return jsonify (
        { "sucess CORS" : True }
    )


