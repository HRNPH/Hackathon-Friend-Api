# import fast api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pymongo

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
    password = 'signal2020'
    client = pymongo.MongoClient(f"mongodb://hrnph:{password}:@hackathonfriend-shard-00-00.5juva.mongodb.net:27017,hackathonfriend-shard-00-01.5juva.mongodb.net:27017,hackathonfriend-shard-00-02.5juva.mongodb.net:27017/?ssl=true&replicaSet=atlas-ka8mw2-shard-0&authSource=admin&retryWrites=true&w=majority")
    db = client.test
    data = client['contents']
    return data


# create index route
@app.get("/")
def index():
    return {"routes": '/api'}

# create /api routes
@app.get("/home")
def get_home():
    # return data.image
    data = get_article()
    return {'data': data}