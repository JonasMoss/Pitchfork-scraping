# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 21:32:29 2016

@author: Jonas
"""

# We start our session in this file. 
session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
           
# The connection to mongodb is createdher.
conn = MongoClient()
pitchfork = conn.pitchfork
reviews = pitchfork.review

# Here starts the iteration


failures = []
last_iter = 0
for i in range(91,1530):
    req = session.get("http://pitchfork.com/reviews/albums/?page={}".format(i), headers=headers)
    bsObj = BeautifulSoup(req.text,"lxml")
        
    if (bsObj.title.get_text()=='Page not found | Pitchfork'): 
        # The pages won't go on forever. Here we make sure that the program terminates.
        last_iter = i
        print("The last iteration is: {}".format(i))
        break
    
    else:
        # If not, everything is fine and dandy!
        print("Running iteration {}...".format(i))
        review_links = ["http://www.pitchfork.com" + a['href'] for a in bsObj.find_all("a",{"class":"album-link"})]
    
        for url in review_links:
            try:
                insert_record(url)
            except:
                print("Failure at: {}".format(url))
                failures.append(url)

# Take care of falures:
failures_two = []
for url in failures:
    try:
        insert_record(url)
    except:
        print("Failure at: {}".format(url))
        failures_two.append(url)
    