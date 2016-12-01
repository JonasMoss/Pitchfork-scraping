# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 14:42:07 2016

@author: Jonas
"""

import requests
import json
from bs4 import BeautifulSoup


session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

# This is an example URL. Every album review appears to ahhere to the same format.          
url = "http://pitchfork.com/reviews/albums/21333-painting-with/"

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
year        = int(tombstone['album']['release_year'])
rating      = float(tombstone['rating']['rating'])

# Contains information about the reviewer.
authors     = [item['name'] for item in json_junk['items'][itemPages]['authors']]
author_urls = [item['url'] for item in json_junk['items'][itemPages]['authors']]
genres      = [item['display_name'] for item in json_junk['items'][itemPages]['genres']]
abstract    = json_junk['items'][itemPages]['abstract'].replace("\xa0"," ")
year        = json_junk['items'][itemPages]['pub_date']

# Body of the review. They are slightly different in formatting.
review      = json_junk['items'][itemPages]['body']['en'].replace("\xa0"," ")
#body2 = bsObj.find(name="div",attrs={"class":"contents dropcap"})