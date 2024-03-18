import asyncio
import json
import os
import re

from aiohttp_requests import requests
from bs4 import BeautifulSoup

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 '
                  'Safari/537.36'}

# If only need a certain generation of card translation, just enter the new generation card list form link.
# Example: https://battlespiritsnova.com/search.php?input_set=BS65
# url_list = ['https://battlespiritsnova.com/search.php?input_set=CB30']
url_list = ['https://battlespiritsnova.com/search.php?input_sign=%3E%3D&input_cost=0']
failed_url_list = []
card_list = {}
try:
    with open(f'{os.path.dirname(os.path.realpath(__file__))}/effect_json/chinese.json', 'r', encoding='utf-8') as f:
        card_list = json.load(f)
except Exception as err:
    print(f"FILE ERROR: {err}")
    input()
    pass


async def get_card(id_, effect):
    card_list.update({id_: effect})


async def fetch_page(url):
    while True:
        try:
            response = await requests.get(url, headers=header)
            responseText = response.text()
            break
        except Exception as err:
            print(f"ERR: {err} at URL: {url}")
            failed_url_list.append(url)
            pass
    return await responseText


async def parse_page(text):
    card_list_xml = BeautifulSoup(text, features="html.parser").find_all('table', class_="BSbigTable_search")
    for card in card_list_xml:
        id_ = card.find('table', class_="BSTable_search").find('td').get_text(strip=True)
        effect = card.find('div', class_="effect_tab")
        #         print(effect)
        effect = BeautifulSoup(str(effect).replace("<br>", "\n\r").replace("<br/>", "\n\r"), features='lxml')
        effect = effect.text.strip()
        await get_card(id_, effect)


async def fetch_and_parse(url):
    text = await fetch_page(url)
    await parse_page(text)


async def main(url_list):
    tasks = []
    for gen in url_list:
        text = await fetch_page(gen)
        last_page = int(re.search(r'page=(\d+)',
                                  BeautifulSoup(text, features="html.parser").find('div', class_="pagination").find_all(
                                      'a')[-1].get('href')).group(1))
        for page in range(1, last_page + 1, 30):
            page_count = page + 30
            if page + 30 > last_page:
                page_count = last_page + 1
            for page_ in range(page, page_count):
                # await fetch_and_parse(gen+f"&page={page_}")
                tasks.append(fetch_and_parse(gen + f"&page={page_}"))
            await asyncio.gather(*tasks)
            print(gen, "done", page, page_count)
            tasks = []
    while len(failed_url_list):
        for url in failed_url_list:
            await fetch_and_parse(url)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(url_list))

with open(f'{os.path.dirname(os.path.realpath(__file__))}/effect_json/chinese.json', 'w', encoding='utf-8') as f:
    json.dump(card_list, f, ensure_ascii=False)
