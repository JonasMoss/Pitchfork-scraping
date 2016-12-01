# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 14:42:07 2016

@author: Jonas
"""

import requests
import json
from bs4 import BeautifulSoup

def get_record_from_url(url):
    """ 
    Supply a json_junk, which must be a url of exactly the right format. 
    The function returns a record that will be inserted into the mongodb.
    """
    
    req = session.get(url, headers=headers)
    bsObj = BeautifulSoup(req.text,"lxml")

    # All the interesting information lies in a JSON-object locted at the 7th 
    # <script>-tag, and furhter inside stuff like 'context','dispatcher', etc. 
    # All of this formating is likely to change in the future. (27.11.2016 today)-

    json_junk = bsObj.find_all(name="script")
    json_junk = json_junk[7].get_text().strip("<script>window.App=").strip(";</script>")
    json_junk = json.loads(json_junk)['context']['dispatcher']['stores']['ReviewsStore']
    
    # This itemPages id is an internal reference to this particular review.
    itemPages   = str(json_junk['itemPages'][0])

    # Contains loads of info about different things, such as rating, album name, 
    # artists, publisher and year of publication. This tombstone can be decomposed 
    # just as we wish...

    tombstone   = json_junk['items'][itemPages]['tombstone']['albums'][0]
    album       = tombstone['album']['display_name']
    artists     = [item['display_name'] for item in tombstone['album']['artists']]
    labels      = [item['display_name'] for item in tombstone['album']['labels']]
    genres      = [item['display_name'] for item in json_junk['items'][itemPages]['genres']]
    year        = (tombstone['album']['release_year'])
    pub_date    = json_junk['items'][itemPages]["pub_date"]
    rating      = (tombstone['rating']['rating'])

    # Contains information about the reviewer.
    authors     = [item['name'] for item in json_junk['items'][itemPages]['authors']]
    author_urls = [item['url'] for item in json_junk['items'][itemPages]['authors']]

    # Body of the review. They are slightly different in formatting.
    abstract    = json_junk['items'][itemPages]['abstract'].replace("\xa0"," ")
    review      = json_junk['items'][itemPages]['body']['en'].replace("\xa0"," ")
    #review2 = bsObj.find(name="div",attrs={"class":"contents dropcap"})
    
    record      = {"itemPages" : int(itemPages),
                   "album" : album,
                   "artists" : artists,
                   "labels" : labels,
                   "genres" : genres,
                   "year" : year,
                   "rating" : rating,
                   "reviewers" : authors,
                   "reviewer_urls": author_urls,
                   "review" : review,
                   "pub_date" : pub_date,
                   "abstract" : abstract,
                   "url" : url,
                   "json_junk": json_junk
                   }
    return(record)
    

def insert_record(url):
    """
    The url points to a Pitchfork review, and a suitably formated record
    is placed into the mongodb. 
    """
    
    record = get_record_from_url(url)
    
    try: 
        insertion = reviews.insert_one(record).inserted_id
    except:
        insertion = "Duplicate key."
        
    return(insertion)
                   