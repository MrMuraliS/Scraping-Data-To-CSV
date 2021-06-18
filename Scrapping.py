import requests
from bs4 import BeautifulSoup
import pprint
import pandas as pd

url = 'https://gadgets.ndtv.com/mobiles/apple-phones'
req = requests.get(url)

soup = BeautifulSoup(req.content, 'html.parser')
iPhone_links = soup.select('.rvw-imgbox')

temp = pd.DataFrame()
extract_data = []
links_result = []
for i in range(len(iPhone_links)):
    links = iPhone_links[i].select('a')
    if links:
        final_link = links[0].get('href')
        links_result.append(final_link)
        # pprint.pprint(len(links_result))

        try:
            # url = 'https://gadgets.ndtv.com/apple-iphone-11-price-in-india-91110'
            req = requests.get(final_link)

            res = BeautifulSoup(req.content, 'html.parser')
            details = res.select('._st-wrp')

            table_details = details[0].select('tbody')
            keys = []
            values = []
            for idx, item in enumerate(table_details):
                try:
                    rows_data = table_details[idx].select('tr')
                    if rows_data:
                        for idx2, item2 in enumerate(rows_data):
                            data = rows_data[idx2].select('td')
                            if data:
                                value1 = data[0].getText()
                                value2 = data[1].getText()
                                if value1 in ('Brand', 'Model', 'Price in India', 'Release date', 'Fast charging',
                                              'Wireless charging', 'Pixels per inch (PPI)', 'Internal storage',
                                              'Operating system'):
                                    keys.append(value1)
                                    values.append(value2)

                except IndexError:
                    break
            df = pd.DataFrame(data=[values], columns=[keys])
            temp = temp.append(df)
        except:
            print('something went wrong')

print('Process is done')
temp.to_csv('iPhonesData.csv')