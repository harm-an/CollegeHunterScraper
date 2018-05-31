from bs4 import BeautifulSoup

import urllib
import re
from selenium import webdriver
import json
import requests


data = json.load(open('database.json'))

branchesSet = set()
locationSet = set()

for college in data['colleges']:
	locationSet.add(college['state'])
	for branch in college['branches']:
		branchesSet.add(branch)

branches = []
states = []
for branch in branchesSet:
	branches.append(branch)

for state in locationSet:
	states.append(state)

branches.sort()
states.sort()
finalDataJSON = json.dumps(branches,indent=4, sort_keys=True)
statesJSON = json.dumps(states,indent=4, sort_keys=True)
#finalDataJSON2 = json.dumps(colleges2,indent=4, sort_keys=True)

with open("branches.json", "w") as myfile:
    myfile.write(finalDataJSON)

with open("states.json", "w") as myfile:
    myfile.write(statesJSON)


print(len(data['colleges']))