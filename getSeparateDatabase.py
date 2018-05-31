from bs4 import BeautifulSoup

import urllib
import re
from selenium import webdriver
import json
import requests


data = json.load(open('database.json'))

colleges = [];

colleges2 = [];

for college in data['colleges']:
	if college['examType'] == 'JEE Advanced':
		colleges.append(college)
	else:
		colleges2.append(college)

finalDataJSON = json.dumps(colleges,indent=4, sort_keys=True)
finalDataJSON2 = json.dumps(colleges2,indent=4, sort_keys=True)

with open("advanced_database.json", "w") as myfile:
    myfile.write(finalDataJSON)
with open("main_database.json", "w") as myfile:
    myfile.write(finalDataJSON2)

print(len(data['colleges']))