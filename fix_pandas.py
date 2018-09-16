#import numpy
#print(numpy)

for i in new_names_list:
    i = ''.join(i)
    print(type(i))
    url = 'https://www.basketball-reference.com/' + name_dict[i]
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'html.parser')
    player_data = []
    stat_content = soup.find('div', attrs={'id': 'all_per_game'})
    stat_table = stat_content.find('div', attrs={'class': 'table_outer_container'})
    stat_table = stat_table.find('tbody')