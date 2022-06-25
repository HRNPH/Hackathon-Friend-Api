# import fast api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pymongo
import urllib
import os

# create app
app = FastAPI()
# allow crossorigin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# connect to monogdb server db and return all contents
def get_article():
    qrstring = "mongodb+srv://hrnph:signal2020@hackathonfriend.5juva.mongodb.net/?retryWrites=true&w=majority"
    # urlendcode qrstring
    qrstring = urllib.parse.quote_plus(qrstring)
    client = pymongo.MongoClient(qrstring)

    return client


# create index route
@app.get("/")
def index():
    return {"routes": '/home'}

# create /api routes
@app.get("/home")
def get_home():
    # return data.image
    data = get_article()
    return {'data': data}

@app.post("/create_camp")
# receive data from client and create a new camp
def create_camp(data):
    # save data to mongodb
    data = get_article()
    data.insert_one(data)
    return {'data': data}