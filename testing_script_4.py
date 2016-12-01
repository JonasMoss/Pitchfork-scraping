# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 17:16:19 2016

@author: Jonas
"""

import pymongo
from pymongo import MongoClient
db = MongoClient().aggregation_example
result = db.things.delete_many({})
result = db.things.insert_many([{"x": 1, "tags": ["dog", "cat"]},
                                {"x": 2, "tags": ["cat"]},
                                {"x": 3, "tags": ["mouse", "cat", "dog"]},
                                {"x": 4, "tags": []}])
result.inserted_ids

db.things.create_index([('x', pymongo.ASCENDING)],unique=True)

from bson.son import SON
pipeline = [
     {"$unwind": "$tags"},
     {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
     {"$sort": SON([("count", -1), ("_id", -1)])}
]
list(db.things.aggregate(pipeline))

from bson.code import Code
reducer = Code("""
                function (key, values) {
                  var total = 0;
                  for (var i = 0; i < values.length; i++) {
                    total += values[i];
                  }
                  return total;
                }
                """)

results = db.things.group(key={"x":1}, condition={}, initial={"count": 0}, reduce=reducer)
for doc in results:
    print(doc)
