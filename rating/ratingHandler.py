import os
import pymongo
import math

from connect.models import Teacher, Profile

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


def set_ratings(student_email: str, teacher_email: str, vote: int) -> None:
    """

    Args:
        student_email:
        teacher_email:
        vote: +1 if upvote; -1 if downvote; 0 to reset
    """
    db = pymongo.MongoClient(os.environ['MONGODB_URI'])[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    entry = collection.find_one({"_id": student_email})
    prev_vote=0
    if not entry:
        entry = dict()
    else:
        collection.delete_one({"_id": student_email})
    if entry.get(teacher_email):
        prev_vote = entry.get(teacher_email)
    entry[teacher_email] = vote
    collection.insert_one(entry)
    profile = Profile.objects.get(email=teacher_email)
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
    teacher.confidence = worker.return_confidence(teacher, use_cache=False, confidence_only=True)
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
            return element_confidence, element.UpVotes, 1/element.DownVotes

    # Disabled for now as I don't know how to sort a ManyToMany Field
    # def sort(self):
    #     cache = Worker
    #     for skill in Skill.objects.all():
    #         skill.Teacher_set.sort(key=cache.return_confidence)
    #         skill.save()

    def set_confidence(self):
        worker = Worker()
        for teacher in Teacher.objects.all():
            teacher.confidence = worker.return_confidence(teacher, use_cache=False, confidence_only=True)
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

