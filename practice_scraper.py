from bs4 import BeautifulSoup
import requests
import pandas as pd

page = 'https://www.basketball-reference.com/players/d/duranke01.html'
response = requests.get(page).text
soup = BeautifulSoup(response, 'html.parser')

stat_content = soup.find('div', attrs={'id': 'all_per_game'})
stat_table = stat_content.find('div', attrs={'class': 'table_outer_container'})
stat_table = stat_table.find('tbody')

for i in stat_table.find_all('tr'):
	print i