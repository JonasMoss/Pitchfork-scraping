# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 21:51:06 2016

@author: Jonas
"""
# Deletes all records! Careful.
#reviews.delete_many({})

# Formats each record beautifully.
[' & '.join(review['artists']) + ": " + review['album'] + " (" + str(review['year']) + ")" + " (Rating: " + str(review["rating"]) + ")" for review in reviews.find()]


from pymongo import MongoClient
conn = MongoClient()
pitchfork = conn.pitchfork
reviews = pitchfork.review

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

ratings = [float(review["rating"]) for review in reviews.find()]
ratings = Counter(ratings)
reviewers = ['&'.join(review["reviewers"]) for review in reviews.find()]
reviewers = Counter(reviewers)
substantial_reviewers = {(key,value) for (key, value) in dict(reviewers).items() if value >= 10}

genres =  [' & '.join(review["genres"]) for review in reviews.find()]
genres = Counter(genres)
genres_unique = ["Rock","Electronic","Jazz","Global","Folk/Country","Pop/R&B","Experimental","Metal","Rap"]

genre_ratings = dict([(genre,Counter([float(review["rating"]) for review in reviews.find({"genres":{"$in":[genre]}})])) for genre in genres_unique])

for genre in genres_unique:
    plt.bar(genre_ratings[genre].keys(), genre_ratings[genre].values(), width=0.1, color="blue")


substantial_reviewers = {(key,value) for (key, value) in dict(reviewers).items() if value >= 10}


# List of all 10.0-albums.
perfect_albums = [' & '.join(review['artists']) + ": " + review['album'] + " (" + str(review['year']) + ")" + " (Rating: " + str(review["rating"]) + ")" for review in reviews.find({"rating": "10.0"})]

# Do the HTML-cleaning.
import re

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext
  
raw_html = reviews.find_one()['abstract']
cleantext = cleanhtml(raw_html)

# Reading difficulty...
from textstat.textstat import textstat
import nltk.tokenize as nt

test_data = cleanhtml(reviews.find_one()['abstract'])
test_data = test_data.replace("\r\n","")
tstats_examples = {"flesch_reading_ease": textstat.flesch_reading_ease(test_data),
                    "smog_index": textstat.smog_index(test_data),
                    "flesch_kincaid_grade": textstat.flesch_kincaid_grade(test_data),
                    "coleman_liau_index": textstat.coleman_liau_index(test_data),
                    "automated_readability_index": textstat.automated_readability_index(test_data),
                    "dale_chall_readability_score": textstat.dale_chall_readability_score(test_data),
                    "difficult_words":textstat.difficult_words(test_data),
                    "linsear_write_formula":textstat.linsear_write_formula(test_data),
                    "gunning_fog":textstat.gunning_fog(test_data),
                    "text_standard":textstat.text_standard(test_data),
                    "char_count":len(test_data),
                    "lexicon_count": textstat.lexicon_count(test_data),
                    "sentence_count": textstat.sentence_count(test_data)
                    }
                    
                    

sentence_count = [textstat.sentence_count(review["abstract"]) for review in reviews.find()]
sentence_count = Counter(sentence_count)
from itertools import groupby
import pandas as pd
shit = groupby(sentence_count,ratings)

for i in shit: print(i[1])

fleschs = dict([(genre,[textstat.flesch_reading_ease(cleanhtml(review['abstract'])) for review in reviews.find({"genres":{"$in":[genre]}})]) for genre in genres_unique])

fleschs_rock = [textstat.flesch_reading_ease(cleanhtml(review['abstract'])) for review in reviews.find({"genres":{"$in":["Rock"]}}) if len(review['abstract']) > 1000]
fleschs_rap = [textstat.flesch_reading_ease(cleanhtml(review['abstract'])) for review in reviews.find({"genres":{"$in":["Rap"]}}) if len(review['abstract']) > 1000]
fleschs_jazz = [textstat.flesch_reading_ease(cleanhtml(review['abstract'])) for review in reviews.find({"genres":{"$in":["Jazz"]}}) if len(review['abstract']) > 1000]
fleschs_metal = [textstat.flesch_reading_ease(cleanhtml(review['abstract'])) for review in reviews.find({"genres":{"$in":["Metal"]}}) if len(review['abstract']) > 1000]

plt.figure(1)
plt.hist(fleschs_rock,50,normed=1)
plt.hist(fleschs_rap,50,normed=1)
plt.show()

maybe_rock = [textstat.sentence_count(cleanhtml(review['abstract'])) for review in reviews.find({"genres":{"$in":["Rock"]}}) if len(review['abstract']) > 1000]
rats_rock = [float(review['rating']) for review in reviews.find({"genres":{"$in":["Rock"]}}) if len(review['abstract']) > 1000]
                     
maybe_experimental = [textstat.sentence_count(cleanhtml(review['abstract'])) for review in reviews.find({"genres":{"$in":["Experimental"]}}) if len(review['abstract']) > 1000]
rats_experimental = [float(review['rating']) for review in reviews.find({"genres":{"$in":["Experimental"]}}) if len(review['abstract']) > 1000]
                     
maybe_electronic = [textstat.sentence_count(cleanhtml(review['abstract'])) for review in reviews.find({"genres":{"$in":["Electronic"]}}) if len(review['abstract']) > 1000]
rats_electronic = [float(review['rating']) for review in reviews.find({"genres":{"$in":["Electronic"]}}) if len(review['abstract']) > 1000]

plt.figure(1)
plt.scatter(rats_rock,maybe_rock,color="red")
plt.scatter(rats_experimental,maybe_experimental,color="green")
plt.scatter(rats_electronic,maybe_electronic,color="blue")
plt.show()

