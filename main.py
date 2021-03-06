import os
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId
from typing import Optional, List
import motor.motor_asyncio
# import cors middle ware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://hrnph:signal2020@hackathonfriend.5juva.mongodb.net/?retryWrites=true&w=majority')
db = client.posts
# allow cross origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class userpost(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    detail: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "ตัวตึง",
                "detail": "หาตัวตึงกว่านี้ไม่มีแล้ว ผมนี่แหละของจริง 200%",
            }
        }



@app.post("/posts", response_description="Add new userpost", response_model=userpost)
async def create_userpost(userpost: userpost = Body(...)):
    userpost = jsonable_encoder(userpost)
    new_userpost = await db["userposts"].insert_one(userpost)
    created_userpost = await db["userposts"].find_one({"_id": new_userpost.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_userpost)


@app.get("/posts", response_description="List all userposts", response_model=List[userpost])
async def list_userposts():
    userposts = await db["userposts"].find().to_list(1000)
    return userposts


@app.get("/posts/{id}", response_description="Get a single userpost", response_model=userpost)
async def show_userpost(id: str):
    if (userpost := await db["userposts"].find_one({"_id": id})) is not None:
        return userpost

    raise HTTPException(status_code=404, detail=f"userpost {id} not found")

@app.delete("/{id}", response_description="Delete a userpost")
async def delete_userpost(id: str):
    delete_result = await db["userposts"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"userpost {id} not found")

# camp posts API
# class camppost(BaseModel):
#     id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
#     title: str = Field(...)
#     detail: str = Field(...)

#     class Config:
#         allow_population_by_field_name = True
#         arbitrary_types_allowed = True
#         json_encoders = {ObjectId: str}
#         schema_extra = {
#             "example": {
#                 "name": "ตัวตึง",
#                 "detail": "หาตัวตึงกว่านี้ไม่มีแล้ว ผมนี่แหละของจริง 200%",
#             }
#         }



# @app.post("/camps", response_description="Add new camppost", response_model=camppost)
# async def create_camppost(camppost: camppost = Body(...)):
#     camppost = jsonable_encoder(camppost)
#     new_camppost = await db["campposts"].insert_one(camppost)
#     created_camppost = await db["campposts"].find_one({"_id": new_camppost.inserted_id})
#     return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_camppost)


# @app.get("/camps", response_description="List all campposts", response_model=List[camppost])
# async def list_campposts():
#     campposts = await db["campposts"].find().to_list(1000)
#     return campposts


# @app.get("/camps/{id}", response_description="Get a single camppost", response_model=camppost)
# async def show_camppost(id: str):
#     if (camppost := await db["campposts"].find_one({"_id": id})) is not None:
#         return camppost

#     raise HTTPException(status_code=404, detail=f"camppost {id} not found")

# @app.delete("/camps/{id}", response_description="Delete a camppost")
# async def delete_camppost(id: str):
#     delete_result = await db["campposts"].delete_one({"_id": id})

#     if delete_result.deleted_count == 1:
#         return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

#     raise HTTPException(status_code=404, detail=f"camppost {id} not found")