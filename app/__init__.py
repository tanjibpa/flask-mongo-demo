from flask import Flask
from .main import main
from .auth import auth
from flask_bootstrap import Bootstrap
# from flask_pymongo import PyMongo
import pymongo
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']  
# app.config['MONGO_DBNAME'] = os.environ['MONGO_DBNAME']
# app.config['MONGO_URL'] = os.environ['MONGO_URL']
# bootstrap.init_app(app)
Bootstrap(app)
# mongo = PyMongo(app)
client = pymongo.MongoClient(os.environ['MONGO_URL'])
db = client['journo']
collection = db['journo']

app.register_blueprint(main)
app.register_blueprint(auth)