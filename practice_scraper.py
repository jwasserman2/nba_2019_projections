# Notebook can be found at https://mybinder.org/v2/gh/jwasserman2/nba_2019_projections/master
import sys
#for notebook: !{sys.executable} -m pip install beautifulsoup4
from bs4 import BeautifulSoup
import requests
#for notebook: !{sys.executable} -m pip install pandas
#import pandas as pd
#for notebook: !{sys.executable} -m pip install tabulate
from tabulate import tabulate

##############################################
#--------------------------------------------#
#----Gathering Player Names and BRef URLs----#
#--------------------------------------------#
##############################################
names_page = 'https://www.basketball-reference.com/leagues/NBA_2018_per_game.html'
names_page_response = requests.get(names_page).text
names_table = BeautifulSoup(names_page_response, 'html.parser').find('tbody')
names_rows = names_table.find_all('tr')

data = []
name_dict = {}
for i in names_rows:
    cols = i.find_all('td', attrs={'data-stat': 'player'})
    for j in cols:
        ref_html = j.find_all('a')
        ref_html = str(ref_html)
        ref_html = ref_html.split('"')[1]
    dict_entry = ref_html
    cols = [ele.text.strip() for ele in cols]
    if cols != []:
        data.append([ele for ele in cols if ele])
        name_dict[''.join(cols)] = dict_entry
    else:
        continue

def dedup_names(names_list, new_names_list):
    for name in names_list:
        if name not in new_names_list:
            new_names_list.append(name)

new_names_list = []
dedup_names(data, new_names_list)

######################################################
#----------------------------------------------------#
#--Scraping Player Data and Compiling Into One List--#
#----------------------------------------------------#
######################################################
all_player_table = []
for i in new_names_list:
    i = ''.join(i)
    url = 'https://www.basketball-reference.com/' + name_dict[i]
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    player_data = []
    stat_content = soup.find('div', attrs={'id': 'all_per_game'})
    stat_table = stat_content.find('div', attrs={'class': 'table_outer_container'})
    stat_table = stat_table.find('tbody')

    rows = stat_table.find_all('tr')
    for row in rows:
        season_cols = row.find_all('th')
        season_cols = [ele.text.strip() for ele in season_cols]
        season_cols = ''.join(season_cols)
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        cols.insert(0, i)
        cols.insert(1, season_cols)
        player_data.append([ele for ele in cols if ele])
    all_player_table.append(player_data)

# Get table column names
url = 'https://www.basketball-reference.com/' + name_dict['Alex Abrines']
page = requests.get(url).text
soup = BeautifulSoup(page, 'html.parser')
table_header = soup.find('div', attrs={'id': 'all_per_game'}).find('div', attrs={'class': 'table_outer_container'}).find('thead')
table_header = table_header.find('tr')
column_names = [ele.text.strip() for ele in table_header.find_all('th')]
column_names.insert(0, 'Name')

joined_player_table = []
for counter, i in enumerate(all_player_table):
	if counter == 0:
		joined_player_table = all_player_table[counter]
	else:
		joined_player_table = joined_player_table + i
joined_player_table.insert(0, column_names)

player_df = pd.DataFrame(joined_player_table)
player_df.to_csv("nba_scraped_player_data.csv")
