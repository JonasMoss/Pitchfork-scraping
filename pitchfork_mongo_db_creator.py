# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 21:18:29 2016

@author: Jonas
"""

"""
In this file we create a mongodb database and collections for the Pitchfork
review!
"""


from pymongo import MongoClient

conn = MongoClient()
pitchfork = conn.pitchfork
reviews = pitchfork.review
reviews.create_index([('itemPages', pymongo.ASCENDING)],unique=True)

