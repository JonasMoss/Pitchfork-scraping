# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 14:43:58 2016

@author: Jonas
"""

from collections import Iterable
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

html = urlopen("http://pitchfork.com/reviews/albums/9454-the-maximum-black-ep/")
bsObj = BeautifulSoup(html,"lxml")
images = bsObj.findAll("img", {"src":re.compile("\.\./img/gifts/img.*\.jpg")})
for image in images:
    print(image["src"])