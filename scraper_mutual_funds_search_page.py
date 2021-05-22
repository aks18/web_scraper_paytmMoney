from bs4 import BeautifulSoup
import pandas as pd
import requests, json, re


return_over_time = ['1m', '3m', '1y', '3y', '5y', 'till_date']
category_id = {'debt': 1, 'equity': 2, 'tax_saver': 3, 'hybrid': 4}
max_page = 5

url = f'https://www.paytmmoney.com/mutual-funds/best-return-funds?bucket={return_over_time[3]}&' \
      f'primary_category_id={category_id["equity"]}&page=1'

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')

print(soup)

key_string = "__NEXT_DATA__ = "
end_char = ";"

text_data = soup.find('script', text=re.compile(key_string)).text

text_data = text_data[len(key_string):text_data.index(end_char)]

info_dict = json.loads(text_data)

# print(info_dict)
#
# print(info_dict['props']['pageProps']['initialMfData']['sections'][1])
