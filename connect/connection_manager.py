import datetime
import os
import pymongo
from bson import ObjectId

DATABASE_NAME = 'connect'
COLLECTION_NAME = 'connection_logs'
db = pymongo.MongoClient(os.getenv('MONGODB_URI'))[DATABASE_NAME]
collection = db[COLLECTION_NAME]

MAX_REQUESTS_PER_DAY = int(os.getenv("MAX_REQUESTS_PER_DAY")) if \
    os.getenv("MAX_REQUESTS_PER_DAY") else 4


def request_connection(student: str, teacher: str, skills: list):
    if type(skills) == str:
        skills = [skills]

    # Throttles requests
    if collection.count_documents({
        "student": student,
        "createdAt": {"$gt":
                      datetime.datetime.utcnow() -
                      datetime.timedelta(days=1)},
        # "approvedAt": None
    }) >= MAX_REQUESTS_PER_DAY:
        print("Connection request from " + student + " to " + teacher +
              " throttled", flush=True)
        return "THROTTLED"

    # Checks if a similar previous request is pending
    if collection.find_one({
        "student": student,
        "teacher": teacher,
        "skills": skills,
        "approvedAt": None
    }, {"_id": 1}):
        print("Connection request from " + student + " to " + teacher +
              " blocked", flush=True)
        return "BLOCKED"

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
    entry = collection.find_one({'_id': oid})
    collection.update_one({'_id': oid},
                          {"$set":
                              {
                                  "approvedAt": datetime.datetime.utcnow()
                              }})
    return entry


def list_approvals_received(student: str) -> list:
    entries = collection.find({"student": student},
                              {"teacher": 1, "_id": 0, "approvedAt": 1})
    teachers = set()
    for entry in entries:
        if entry['approvedAt'] is not None:
            teachers.add(entry['teacher'])
    return list(teachers)


def list_approvals_sent(teacher: str) -> list:
    pass
