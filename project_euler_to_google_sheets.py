import gspread
from oauth2client.service_account import ServiceAccountCredentials

import urllib2
from bs4 import BeautifulSoup
import requests

import re

# Setup the Sheets API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
client = gspread.authorize(creds)

# Load sheet
sheet = client.open("Project Euler Solutions").sheet1

# Scrape Project Euler for solutions
cookies = {}
page = requests.get("https://projecteuler.net/archives",cookies=cookies).content
soup = BeautifulSoup(page,'lxml')
for link in soup.find_all(href=re.compile("problem-*")):
	problem_id=int(link.get('href').split('=')[1])
	new_page = requests.get("https://projecteuler.net/"+link.get('href'),cookies=cookies).content
	new_soup = BeautifulSoup(new_page,'lxml')
	answer = new_soup.select('form > table > tr > td > table > tr > td:nth-of-type(2) > b')[0].text
	# update sheet
	sheet.update_cell(problem_id,1,answer)