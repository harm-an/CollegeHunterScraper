from bs4 import BeautifulSoup

import urllib
import re
from selenium import webdriver
import json
import requests

driver = webdriver.Firefox()

driver.get('https://josaa.nic.in/Result2016/result/OpeningClosingRank.aspx')

html = driver.page_source

soup = BeautifulSoup(html, 'lxml')

#anchors = [section.find('a', {'class':'tuple-institute-name'}) for section in soup.findAll("section", {'class': 'tuple-clg-name'})]


#for anchor in anchors:
#	print(anchor.contents[0])
colleges = set()
finalData = {}
data = []


for link in soup.find_all('td', {'align': 'left'}):
	if re.match('[a-zA-Z]', link.contents[0]):
		colleges.add(link.contents[0])

#colleges = set(filter(re.match('[a-zA-Z]'), colleges))
for college in colleges:
	collegeData = {}
	collegeData['name'] = college
	data.append(collegeData)

finalData['colleges'] = data



test = []
for link in soup.find_all('tr'):
	h = {}
	i=0
	for x in link.find_all('td', {'align': 'left'}):
		if i == 0:
			h['name'] = x.contents[0]
		else:
			for y in x.find_all('span'):
				h['program'] = y.contents[0]
		i = i+1
	j = 0
	for x in link.find_all('td', {'align': 'center'}):
		if j == 0:
			for y in x.find_all('span'):
				h['quota'] = y.contents[0]
		if j == 1:
			for y in x.find_all('span'):
				h['opening rank'] = y.contents[0]
		if j == 2:
			for y in x.find_all('span'):
				h['closing rank'] = y.contents[0]
		j = j+1
	test.append(h)

testJ = {}
testJ['test'] = test
testJSON = json.dumps(testJ,indent=4, sort_keys=True)
#print(testJSON)
#print(len(testJ['test']))



#for value2 in testJ['test']:
#	print(value2[0])
		
for name in colleges:
	#print(name + '----------------')
	branchesSet = set()
	for value in test:
		if 'name' in value:
			if value['name'] == name:
				branchesSet.add(value['program'])
	branches = []
	for branch in branchesSet:
		branches.append(branch)
	#print(branches)
	for college in finalData['colleges']:
		if college['name'] == name:
			college['branches'] = branches

colleges_b = []
for college in finalData['colleges']:
	college_b = {}
	college_b['name'] = college['name']
	branchesRank = []
	for branch in college['branches']:
		branchRank = {}
		branchRank['name'] = branch
		quotaList = []
		for tpl in testJ['test']:
			quota = {}
			if 'name' in tpl:
				if tpl['name'] == college['name']:
					if tpl['program'] == branch:
						quota['name'] = tpl['quota']
						quota['opening rank'] = tpl['opening rank']
						quota['closing rank'] = tpl['closing rank']
						quotaList.append(quota)
		branchRank['quota'] = quotaList
		branchesRank.append(branchRank)
	college_b['branchRank'] = branchesRank
	colleges_b.append(college_b)

branchRanksData = {}
branchRanksData['value'] = colleges_b


for value in branchRanksData['value']:
	for college in finalData['colleges']:
		if college['name'] == value['name']:
			college['branchWiseRank'] = value['branchRank']
			name_words = college['name'].split()
			if name_words[-1] == 'Pradesh' or name_words[-1] == 'Bengal':
				college['location'] = name_words[-2] +" "+ name_words[-1]
			else:
				college['location'] = name_words[-1]

citiesData = json.load(open('cities.json'))

collegeLinks = json.load(open('collegeLinks.json'))

for college in finalData['colleges']:
	i = 0
	for city in citiesData:
		if college['location'] == city['name']:
			college['state'] = city['state']
			i=1
	if i != 1:
		college['state'] = college['location']
	#print(college['location'] + '---' + college['state'])


for college in finalData['colleges']:
	for links in collegeLinks:
		if college['name'] == links['name']:
			college['link'] = 'http://josaa.nic.in/SeatInfo/root/InstProfile.aspx?instcd='+links['link']


for college in finalData['colleges']:
	if 'link' in college:
		url_college = college['link']

		req  = requests.get(url_college, verify = False)

		datalink = req.text

		soup = BeautifulSoup(datalink, 'lxml')

		for x in soup.find_all('span', {'id': 'ctl00_ContentPlaceHolder1_lblCompleteMailingAddr'}):
			#print('hello')
			college['address'] = x.contents[0]
		for y in soup.find_all('span', {'id': 'ctl00_ContentPlaceHolder1_lblEmail'}):
			college['email'] = y.contents[0]


id = 1
for college in finalData['colleges']:
	name_words = college['name'].split()
	if name_words[0] == 'Indian' and name_words[1] == 'Institute' and name_words[2] == 'of' and name_words[3] == 'Technology':
		college['examType'] = 'JEE Advanced'
	else:
		college['examType'] = 'JEE Main'
	college['totalPrograms'] = len(college['branches'])
	college['_id'] = 'ICG-'+str(id)
	id = id+1

finalDataJSON = json.dumps(finalData,indent=4, sort_keys=False)
#print(finalDataJSON)

with open("database.json", "w") as myfile:
    myfile.write(finalDataJSON)


#branchesRankJSON = json.dumps(branchRanksData,indent=4, sort_keys=True)
#print(branchesRankJSON)



#print(len(finalData['colleges']))




driver.quit()




