# Notebook can be found at https://mybinder.org/v2/gh/jwasserman2/nba_2019_projections/master
import sys
#for notebook: !{sys.executable} -m pip install beautifulsoup4
from bs4 import BeautifulSoup
import requests
#for notebook: !{sys.executable} -m pip install pandas
import pandas as pd
#for notebook: !{sys.executable} -m pip install tabulate
from tabulate import tabulate

page = 'https://www.basketball-reference.com/players/d/duranke01.html'
response = requests.get(page).text
soup = BeautifulSoup(response, 'html.parser')

stat_content = soup.find('div', attrs={'id': 'all_per_game'})
stat_table = stat_content.find('div', attrs={'class': 'table_outer_container'})
stat_table = stat_table.find('tbody')

#for i in stat_table.find_all('tr'):
#	print i

#########################
#-----------------------#
#----Gathering Pages----#
#-----------------------#
#########################
names_page = 'https://www.basketball-reference.com/leagues/NBA_2018_per_game.html'
names_page_response = requests.get(names_page).text
names_table = BeautifulSoup(names_page_response, 'html.parser').find('tbody')
names_rows = names_table.find_all('tr')
data = []
for i in names_rows:
	cols = i.find_all('td', attrs={'data-stat': 'player'})
	cols = [ele.text.strip() for ele in cols]
	data.append([ele for ele in cols if ele])

def dedup_names(names_list, new_names_list):
    for name in names_list:
        if name not in new_names_list:
            new_names_list.append(name)

new_names_list = []
dedup_names(data, new_names_list)

def namefix(list, dict):
    for name in list:
        try:
            fixed_name = ''.join(name)
            fixed_name = fixed_name.replace('-', '')
            fixed_name = fixed_name.replace("'", "")
            fixed_name = fixed_name.lower()
            fixed_name = fixed_name.split()[1][0:5] + fixed_name.split()[0][0:2]
            if fixed_name + '01' in dict.values():
                dict[''.join(name)] = fixed_name + '02'
            else:
                dict[''.join(name)] = fixed_name + '01'
        except IndexError:
            list.remove(name)

name_dict = {}
namefix(new_names_list, name_dict)

