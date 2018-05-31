from bs4 import BeautifulSoup

import urllib
import re
from selenium import webdriver
import json

driver = webdriver.Firefox()

driver.get('http://josaa.nic.in/SeatInfo/root/InstituteView.aspx')

html = driver.page_source

soup = BeautifulSoup(html, 'lxml')
for linebreak in soup.find_all('br'):
	linebreak.extract()

i = 2

collegeLink = []

while i<99:	
	college = {}
	if i<10:	
		link = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_gvInstTypelist_ctl0' + str(i) +'_lblinstcd'})
		#print(link.contents[1].strip())
		college['name'] = link.contents[1].strip()
		college['link'] = link.contents[0].strip()
	else:
		link = soup.find('span', {'id': 'ctl00_ContentPlaceHolder1_gvInstTypelist_ctl' + str(i) +'_lblinstcd'})
		#print(link.contents[1].strip())
		college['name'] = link.contents[1].strip()
		college['link'] = link.contents[0].strip()
	collegeLink.append(college)
	i = i+1


finalDataJSON = json.dumps(collegeLink,indent=4, sort_keys=True)

with open("collegeLinks.json", "w") as myfile:
    myfile.write(finalDataJSON)

#print(finalDataJSON)
driver.quit()