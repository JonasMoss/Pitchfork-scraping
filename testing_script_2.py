# -*- coding: utf-8 -*-
"""
Created on Sun Nov 27 11:07:48 2016

@author: Jonas
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS(executable_path='phantomjs.exe')
cont = driver.get("http://pitchfork.com/reviews/albums/22531-oneida-rhys-chatham-whats-your-sign/")

try:
    element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "loadedButton")))
finally:
    print(driver.find_element_by_id("content").text)
    driver.close()
    
from selenium import webdriver

headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}

for key, value in enumerate(headers):
    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value
                                            

driver = webdriver.PhantomJS(executable_path='phantomjs.exe')
cont = driver.get("http://pitchfork.com/reviews/albums/22531-oneida-rhys-chatham-whats-your-sign/")