from flask import Flask
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["tpo_portal"]
users = db["users"]
