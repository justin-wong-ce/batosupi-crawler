import asyncio
import json
import os
import re
from random import random
from time import sleep

from aiohttp_requests import requests
from bs4 import BeautifulSoup

headers = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) '
                      'Version/9.0.2 Safari/601.3.9'
    },
    {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'
    },
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/47.0.2526.111 Safari/537.36 '
    },
    {
        'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/51.0.2704.64 Safari/537.36 '
    }
]
PREFIX = 'https://battlespiritsnova.com/search.php?input_set='


async def get_card(id_, effect, card_list):
    card_list.update({id_: effect})


async def fetch_page(url, failed_url_set):
    if len(url) < 28 and url[:8] != 'https://':
        print(f"ERR: BAD URL - {url}")
        failed_url_set.discard(url)
        return "BAD - SKIP"
    for i in range(10):
        try:
            response = await requests.get(url, headers=headers[int(random() * 4.999999)])
            responseText = await response.text()
            failed_url_set.discard(url)
            break
        except Exception as error:
            print(f"ERR (fetch_page): {error} at URL: {url}, #retries={i}")
            failed_url_set.add(url)
            responseText = "BAD - SKIP"
        sleep(1)
    return responseText


async def parse_page(text, card_list, failed_url_set, url):
    if text == "BAD - SKIP":
        return

    card_list_xml = BeautifulSoup(text, features="html.parser").find_all('table', class_="BSbigTable_search")
    if not len(card_list_xml):
        failed_url_set.add(url)
        return
    for card in card_list_xml:
        id_ = card.find('table', class_="BSTable_search").find('td').get_text(strip=True)
        effect = card.find('div', class_="effect_tab")
        #         print(effect)
        effect = BeautifulSoup(str(effect).replace("<br>", "\n\r").replace("<br/>", "\n\r"), features='lxml')
        effect = effect.text.strip()
        await get_card(id_, effect, card_list)
    failed_url_set.discard(url)


async def fetch_and_parse(url, failed_url_set, card_list):
    text = await fetch_page(url, failed_url_set)
    await parse_page(text, card_list, failed_url_set, url)


async def main(url_list, card_list, failed_url_set):
    tasks = []
    for gen in url_list:
        text = await fetch_page(gen, failed_url_set)
        last_page = int(re.search(r'page=(\d+)',
                                  BeautifulSoup(text, features="html.parser").find('div', class_="pagination").find_all(
                                      'a')[-1].get('href')).group(1))
        for page in range(1, last_page + 1, 30):
            page_count = page + 30
            if page + 30 > last_page:
                page_count = last_page + 1
            for page_ in range(page, page_count):
                await fetch_and_parse(gen+f"&page={page_}", failed_url_set, card_list)
                # tasks.append(fetch_and_parse(gen + f"&page={page_}", failed_url_set, card_list))
            await asyncio.gather(*tasks)
            print(gen, "done", page, page_count)
            tasks = []
    for _ in range(20):
        failed_url_set = set(failed_url_set)
        print(f"Failed to get cards from {len(failed_url_set)} pages... "
              f"waiting 5s before retrying failed pages.")
        sleep(5)
        print(sorted(failed_url_set))
        print("...")
        for url in set(failed_url_set):
            await fetch_and_parse(url, failed_url_set, card_list)
        if not len(failed_url_set):
            break

    failed_url_set = set(failed_url_set)
    with open('failed_urls.log', 'w') as failed_url_file:
        for item in failed_url_set:
            failed_url_file.write("%s\n" % item)


def scrape_chinese_effect(gen_name):
    try:
        with open(f'{os.path.dirname(os.path.realpath(__file__))}/effect_json/chinese.json', 'r',
                  encoding='utf-8') as f:
            card_list = json.load(f)
    except Exception as err:
        print(f"FILE ERROR: {err}")
        exit(1)
    failed_url_set = set()
    url_list = [PREFIX + gen_name]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(url_list, card_list, failed_url_set))

    with open(f'{os.path.dirname(os.path.realpath(__file__))}/effect_json/chinese.json', 'w', encoding='utf-8') as f:
        json.dump(card_list, f, ensure_ascii=False)


# # If only need a certain generation of card translation, just enter the new generation card list form link.
# # Example: https://battlespiritsnova.com/search.php?input_set=BS65
# # url_list = ['https://battlespiritsnova.com/search.php?input_set=CB30']
# url_list_test = ['https://battlespiritsnova.com/search.php?input_sign=%3E=&input_cost=0']
#
# try:
#     with open(f'{os.path.dirname(os.path.realpath(__file__))}/effect_json/chinese.json', 'r', encoding='utf-8') as f:
#         card_list_test = json.load(f)
# except Exception as err:
#     print(f"FILE ERROR: {err}")
#     # exit(1)
#     card_list_test = {}
# failed_url_set_test = set()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main(url_list_test, card_list_test, failed_url_set_test))
# # loop.run_until_complete(fetch_and_parse('https://battlespiritsnova.com/search.php?input_set=BSC43&page=15',
# #                                         failed_url_set_test,
# #                                         card_list_test))
# print(failed_url_set_test)
# #
#
# #
# with open(f'{os.path.dirname(os.path.realpath(__file__))}/effect_json/chinese.json', 'w', encoding='utf-8') as f:
#     json.dump(card_list_test, f, ensure_ascii=False)
