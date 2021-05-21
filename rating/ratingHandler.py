import os
import pymongo

DATABASE_NAME = 'rating'
COLLECTION_NAME = 'logs'


def return_ratings(student_email, users) -> dict:
    db = pymongo.MongoClient(os.environ['MONGODB_URI'])[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    entry = collection.find_one({"_id": student_email})
    final_entry = dict()
    if users:
        for i in users:
            final_entry[i] = entry.get(i)
    else:
        final_entry = entry
    return final_entry


def set_ratings(student_email, teacher_email, vote) -> None:
    db = pymongo.MongoClient(os.environ['MONGODB_URI'])[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    entry = collection.find_one({"_id": student_email})
    if not entry:
        entry = dict()
    else:
        collection.delete_one({"_id": student_email})
    entry[teacher_email] = vote
    collection.insert_one(entry)


def worker():
    # TODO: Create function using https://www.evanmiller.org/how-not-to-sort-by-average-rating.html
    pass
