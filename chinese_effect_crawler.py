from bs4 import BeautifulSoup
import json
import re
import asyncio
import aiohttp
from aiohttp_requests import requests
from bs4 import BeautifulSoup
import os

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}
url_list = ['https://battlespiritsnova.com/search.php?input_sign=>%3D&input_cost=0']

async def get_card(id_, effect):
    card_list.update({id_: effect})

async def fetch_page(url):
    while True:
        try:
            response = await requests.get(url)
            break
        except:
            pass
    return await response.text()

async def parse_page(text):
    card_list_xml = BeautifulSoup(text, features="html.parser").find_all('table',class_="BSbigTable_search")
    for card in card_list_xml:
        id_ = card.find('table',class_="BSTable_search").find('td').get_text(strip=True)
        effect = card.find('div',class_="effect_tab")
#         print(effect)
        effect = BeautifulSoup(str(effect).replace("<br>","\n\r").replace("<br/>","\n\r"), features='lxml')
        effect = effect.text.strip()
        await get_card(id_, effect)

async def fetch_and_parse(url):
    text = await fetch_page(url)
    await parse_page(text)
#     print(url, 'done')

async def main(url_list):
    tasks = []
    for gen in url_list:
        text = await fetch_page(gen)
        last_page = int(re.search('page=(\d+)', BeautifulSoup(text, features="html.parser").find('div',class_="pagination").find_all('a')[-1].get('href')).group(1))
        for page in range(1, last_page+1,30):
            page_count =page+30
            if page+30 > last_page:
                page_count = last_page+1  
            for page_ in range(page,page_count):
                tasks.append(fetch_and_parse(gen+f"&page={page_}"))
            await asyncio.gather(*tasks)
            print(gen,"done",page,page_count)
            tasks = []

card_list = {}
loop = asyncio.get_event_loop()
loop.run_until_complete(main(url_list))

with open(f'{os.path.dirname(os.path.realpath(__file__))}/effect_json/chinese.json', 'w', encoding='utf-8') as f:
    json.dump(card_list, f, ensure_ascii=False)