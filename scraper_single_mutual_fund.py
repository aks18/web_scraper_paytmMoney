from bs4 import BeautifulSoup
import pandas as pd
import requests, json, re


url = 'https://www.paytmmoney.com/mutual-funds/scheme/aditya-birla-sun-life-digital-india-fund-direct-growth/inf209k01vf2'

r = requests.get(url)
soup = BeautifulSoup(r.content, 'html5lib')

key_string = "__NEXT_DATA__ = "
end_char = ";"

text_data = soup.find('script', text=re.compile(key_string)).text

text_data = text_data[len(key_string):text_data.index(end_char)]

info_dict = json.loads(text_data)

print(info_dict['props']['pageProps']['initialMfData']['sections'][1])
