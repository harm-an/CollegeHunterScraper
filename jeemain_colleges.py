from bs4 import BeautifulSoup

import urllib
from selenium import webdriver

driver = webdriver.Firefox()

driver.get('https://www.shiksha.com/search/?uaf[]=exam&uaf[]=location&q=Engineering&s[]=2&sa=1%5E0%5E0%5E10%5E0%5E0%5E2%5E0%5E0%5E20%5E0%5E0%5E0%5E0%5Es%3A2&ts=21188843&rf=filters&bc[]=10&ed[]=et_20&ex[]=6244')

html = driver.page_source

soup = BeautifulSoup(html, 'lxml')

#anchors = [section.find('a', {'class':'tuple-institute-name'}) for section in soup.findAll("section", {'class': 'tuple-clg-name'})]


#for anchor in anchors:
#	print(anchor.contents[0])

colleges = []
paidColleges = []

test = {'hello': 'Kuljeet'}
test['hello'] = 'Harman'

for link in soup.find_all("div", {'class': 'clg-tpl'}):
	colleges.append(link)





for college in colleges:
	for section in college.find_all('section', {'class':'tuple-clg-name tpl-paid'}):
		for name in section.find_all('a', {'class':'tuple-institute-name'}):
			colleges.remove(college)


print('college Name \n')

for college in colleges:
	for section in college.find_all('section', {'class':'tuple-clg-name'}):
		for name in section.find_all('a', {'class':'tuple-institute-name'}):
			print(name.contents[0] + '-- ')
			driverCollege = webdriver.Firefox()
			driverCollege.get(name.get('href'))
			html2 = driverCollege.page_source
			soup2 = BeautifulSoup(html2, 'lxml')
			print(soup2.find('span', {'class': 'location-of-clg'}))
			driverCollege.quit()

print(test)
driver.quit()