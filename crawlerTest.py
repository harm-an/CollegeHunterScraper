from bs4 import BeautifulSoup


import requests

url = 'josaa.nic.in/SeatInfo/root/InstProfile.aspx?instcd=231'

r  = requests.get("https://" +url, verify = False)

data = r.text

soup = BeautifulSoup(data, 'lxml')

for link in soup.find_all('img', {'id': 'ctl00_ContentPlaceHolder1_imgLogo'}):
	#print('hello')
	print(link.get('src')[2:])