from flask import Flask
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
# https://flask-httpauth.readthedocs.io/en/latest/
auth = HTTPBasicAuth()
CORS(app)
