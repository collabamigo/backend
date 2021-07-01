import re


from backend import settings

DATABASE_NAME = 'autocomplete'
COLLECTION_NAME = 'trie'


def get_recommendations(query: str, last_id: int = 0):
    if not last_id:
        last_id = 0
    recommendations, cache_id = _return_recommendations(query, last_id)
    return dict(recommendations=recommendations, cache_id=cache_id)


def generate_trie(tags: list, save_to_mongo: bool = True) -> list:
    """
    Generates a trie using a list of words
        :parameter save_to_mongo: Controls if the generated
                                    trie will be saved to MongoDB
        :parameter tags: List of tags/words on which trie is to be generated
        :return: Returns a list of dicts, each depicting a trie node
    """

    db = settings.MongoClient[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    trie = _create_trie(tags)
    if save_to_mongo:
        collection.delete_many({})
        collection.insert_many(trie)
    return trie


def _return_recommendations(query: str, last_id: int):
    if not query:
        return [], 0
    last_id = int(last_id)
    query = query.lower()
    db = settings.MongoClient[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    prev_node = collection.find_one({"_id": last_id})

    if prev_node and query == prev_node['parent_word'] + prev_node['value']:
        # Return same thing
        curr_node = prev_node

    elif prev_node and query.startswith(prev_node['parent_word'] +
                                        prev_node['value']):
        # New characters entered
        new_chars = query[len(prev_node['parent_word'] + prev_node['value']):]
        curr_node = prev_node
        while new_chars:
            curr_node = collection.find_one({"parent_id": curr_node["_id"],
                                             "value":
                                                 {
                                                "$regex": "^" +
                                                re.escape(new_chars[0])}})
            if not curr_node:
                return [], prev_node["_id"]
            check_len = min(len(new_chars), len(curr_node['value']))
            if new_chars[:check_len] != curr_node['value'][:check_len]:
                return [], curr_node["_id"]
            new_chars = new_chars[len(curr_node['value']):]

    elif prev_node and (prev_node['parent_word'] + prev_node['value']). \
            startswith(query):
        # Characters removed
        return _return_recommendations(query, prev_node['parent_id'])

    else:
        # Totally new
        return _return_recommendations(query, 0)

    return curr_node['recommendations'], curr_node['_id']


def _create_trie(tags: list) -> list:
    _Node.curr_id = 0
    tags.sort()
    root = _Node(value="", parent=None)
    root.recommendations = tags[:4]
    result = [root.to_dict()]
    result.extend(_create_trie_helper(tags=tags, parent=root, index=0))
    return result


def _flush_cache(cache, result, index, parent):
    # Cache is ready. Check for compression possibility
    internal_index = index
    # First we verify for non-existence of terminating element exists
    while len(cache[0]) > internal_index + 1:
        mismatch_found = False
        for i in range(1, len(cache)):
            tag = cache[i]
            prev_tag = cache[i - 1]
            if tag[internal_index + 1] != prev_tag[internal_index + 1]:
                mismatch_found = True
                break
        if mismatch_found:
            break
        else:
            internal_index += 1
    child = _Node(parent=parent, value=cache[0][index:internal_index + 1],
                  is_terminal=(len(cache[0]) == internal_index + 1))
    child.recommendations = cache[:4]
    if child.is_terminal:
        cache = cache[1:]
    result.append(child.to_dict())
    result.extend(_create_trie_helper(parent=child,
                                      index=internal_index + 1,
                                      tags=cache))
    return result


def _create_trie_helper(tags, parent, index) -> list:
    if not tags:
        return []
    result = []
    cache = [tags[0]]
    for tag_index in range(1, len(tags)):
        if tags[tag_index][index] != tags[tag_index - 1][index]:
            # Flush and then fill
            result = _flush_cache(cache, result, index, parent)
            cache = [tags[tag_index]]
        else:
            cache.append(tags[tag_index])
    result = _flush_cache(cache, result, index, parent)
    return result


class _Node:
    curr_id = 0

    def __init__(self, value, parent, is_terminal=False):
        self.id = _Node.curr_id
        self.value = value
        self.is_terminal = is_terminal
        self.recommendations = []
        if parent:
            self.parent_id = parent.id
            self.parent_word = parent.parent_word + parent.value
        else:
            self.parent_id = self.parent_word = ""
        _Node.curr_id += 1

    def to_dict(self):
        return dict(_id=self.id,
                    value=self.value,
                    is_terminal=self.is_terminal,
                    parent_id=self.parent_id,
                    parent_word=self.parent_word,
                    recommendations=self.recommendations)


def worker_generate_trie():
    from connect.models import Skill
    generate_trie(list(Skill.objects.values_list('name', flat=True)))


def main():
    while True:
        user_query = input("Q?")
        q_id = input("id?")
        if not q_id:
            q_id = 0
        print(_return_recommendations(user_query, q_id))


if __name__ == "__main__":
    main()
