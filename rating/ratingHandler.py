import os
import pymongo
import math

from connect.models import Teacher, Profile

DATABASE_NAME = 'rating'
COLLECTION_NAME = 'logs'


def return_ratings(student_id, users) -> dict:
    db = pymongo.MongoClient(os.environ['MONGODB_URI'])[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    entry = collection.find_one({"_id": student_id})
    final_entry = dict()
    if users:
        for i in users:
            final_entry[i] = entry.get(i)
    else:
        final_entry = entry
    return final_entry


def set_ratings(student_id: str, teacher_id: str, vote: int) -> None:
    """

    Args:
        student_id:
        teacher_id:
        vote: +1 if upvote; -1 if downvote; 0 to reset
    """
    db = pymongo.MongoClient(os.environ['MONGODB_URI'])[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    entry = collection.find_one({"_id": student_id})
    prev_vote = 0
    if not entry:
        entry = dict()
    else:
        collection.delete_one({"_id": student_id})
    if entry.get(teacher_id):
        prev_vote = entry.get(teacher_id)
    entry[teacher_id] = vote
    collection.insert_one(entry)
    profile = Profile.objects.get(email=teacher_id)
    teacher = Teacher.objects.get(id=profile)
    if vote == +1:
        teacher.UpVotes += 1
    elif vote == -1:
        teacher.DownVotes += 1
    if prev_vote == +1:
        teacher.UpVotes -= 1
    elif prev_vote == -1:
        teacher.DownVotes -= 1
    worker = Worker()
    teacher.confidence = worker.return_confidence(teacher,
                                                  use_cache=False,
                                                  confidence_only=True)
    teacher.save()


class Worker:

    def __init__(self):
        self.cache = dict()

    def return_confidence(self, element, use_cache=True, confidence_only=True):
        element_confidence = None
        if use_cache:
            element_confidence = self.cache.get(str(element.id))
        if element_confidence is None:
            element_confidence = confidence(element.UpVotes, element.DownVotes)
            if use_cache:
                self.cache[str(element.id)] = element_confidence
        if confidence_only:
            return element_confidence
        else:
            return element_confidence, element.UpVotes, 1 / element.DownVotes

    def set_confidence(self):
        worker = Worker()
        for teacher in Teacher.objects.all():
            teacher.confidence = worker.return_confidence(teacher,
                                                          use_cache=False,
                                                          confidence_only=True)
            teacher.save()


def _confidence(ups, downs):
    n = ups + downs

    if n == 0:
        return 0

    z = 1.281551565545
    p = float(ups) / n

    left = p + 1 / (2 * n) * z * z
    right = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    under = 1 + 1 / n * z * z

    return (left - right) / under


def confidence(ups, downs):
    if ups + downs == 0:
        return 0
    else:
        return _confidence(ups, downs)
