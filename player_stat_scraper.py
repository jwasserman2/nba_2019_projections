from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://www.basketball-reference.com/players/d/duranke01.html'
response = requests.get(url).text

print(response)
