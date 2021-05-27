import datetime
import os
import pymongo
from bson import ObjectId

DATABASE_NAME = 'connect'
COLLECTION_NAME = 'connection_logs'
db = pymongo.MongoClient(os.environ['MONGODB_URI'])[DATABASE_NAME]
collection = db[COLLECTION_NAME]


def request_connection(student: str, teacher: str, skills: list):
    if type(skills) == str:
        skills = [skills]

    record = {
        "student": student,
        "teacher": teacher,
        "skills": skills,
        "createdAt": datetime.datetime.utcnow(),
        "approvedAt": None
    }

    return str(collection.insert_one(record).inserted_id)


def accept_connection(oid: str) -> dict:
    oid = ObjectId(oid)
    collection.update_one({'_id': oid},
                          {"$set":
                              {
                                  "approvedAt": datetime.datetime.utcnow()
                              }})
    return collection.find_one({'_id': oid})
