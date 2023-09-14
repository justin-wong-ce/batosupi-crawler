import fandom_crawler
import threading
import requests
import re
import os
import json

dictionary = {}


def scrape_promo(effect_dict):
    # IMG_MODE = False  # True: scrape images; False: scrape effects
    # IMG_MODE not implemented

    html_text = requests.get("https://battle-spirits.fandom.com/wiki/Promo_Cards").text

    # Acquire section names first
    pattern = re.compile(
        r"toclevel-1 tocsection-\d\d?\"><a href=\"#([^\"^\n^\r]*)"
    )

    sections = re.findall(pattern, html_text)

    # Get cards
    pattern = re.compile(
        r"<td>(?:<span style=\"\">)?((?:(?:(?:P|CP|SD|BS|PX|X|GX|EX|PB|KA)?\d\d\d?[RAEDTS]?|BSH|X|PX)(?: \([AB]\))?-?)"
        r"(?:(?:CP|PX|X|RV)?\d?\d\d[RAEDTS]?)?(?: \([AB]\))?)(?:</span>)?\s</td>\s<td><a href=\"([^\"]*)"
    )
    cards = re.findall(pattern, html_text)
    for i in range(len(cards)):
        # card format: [CARD NAME, /wiki LINK TO CARD]
        card_list = list(cards[i])
        if re.search(r"^\d{3}$", card_list[0]) or \
                re.search(r"^\d{2}-\d{2}[RAEDTS]?(?: \([AB]\))?$", card_list[0]) or \
                re.search(r"^17-EXG\d{2}", card_list[0]):
            card_list[0] = "P" + card_list[0]
        elif re.search(r"^X-\d{3}[RAEDTS]?$", card_list[0]):
            card_list[0] = card_list[0].replace("X-", "X")
        elif re.search(r"^PX-\d{2}$", card_list[0]):
            card_list[0] = card_list[0].replace("PX-", "PX19-")
        elif card_list[0] == "CP17-X07":
            card_list[0] = "CP14-X07"
        cards[i] = tuple(card_list)

    # Section does not contain cards, instead a link to wiki
    # [SECTION NAME, /wiki LINK TO CARD SET]
    links = []
    pattern = re.compile(r"class=\"mw-headline\" id=\"(?=(" + "|".join(sections) +
                         r")).*\s*(?:.*\s*)?(?:<ul><li>|<p>)<a href=\"([^\"]*)")
    links.extend(re.findall(pattern, html_text))
    pattern = re.compile("class=\"mw-headline\" id=\"(?=(" + "|".join(sections) +
                         r")).*\s*(?:.*\s*)?<li><a href=\"([^\"]*)")
    links.extend(re.findall(pattern, html_text))
    links = set(links)

    for card in cards:
        # fandom_crawler.fandom_scrape_effect(card[0], card[1], effect_dict)
        threading.Thread(target=fandom_crawler.fandom_scrape_effect, args=(card[0], card[1], effect_dict)).start()

    while True:
        if threading.active_count() == 1:
            break

    for link in links:
        fandom_crawler.fandom_crawler("https://battle-spirits.fandom.com" + link[1], link[0], False, True, False, None)
        print("Processing: " + link[1])


def scrape_all(dictionary):
    # Scrape for all sets from Card_Sets page
    html = requests.get("https://battle-spirits.fandom.com/wiki/Card_Sets").text

    # Get links
    patt = re.compile(r"<a href=\"([^\"]*)\" title=\"([^\"]*)\">")
    urls = re.findall(patt, html)
    urls = set(urls)

    count = 0
    threading_dicts = {} * len(urls)
    for i in range(len(urls)):
        url = urls[i]
        if re.search(r"^/wiki/(?:BS|BSC|SD|PC|PB|CB)\d{2}", url[0]):
            no_tamper = False
        else:
            no_tamper = True
        print("Processing " + str(count) + "/" + str(len(urls)) + ": " + url[0])
        threading.Thread(target=fandom_crawler.fandom_crawler,
                         args=("https://battle-spirits.fandom.com" +
                               url[0], url[1], False, no_tamper, True, threading_dicts[i])).start()
        count = count + 1

    for cards in threading_dicts:
        dictionary.update(cards)


scrape_all(dictionary)
scrape_promo(dictionary)

try:
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/effect_json/english.json", "r", encoding='utf-8') as f:
        effect_dict_curr = json.load(f)
except FileNotFoundError:
    print("File not found")
    pass

dictionary.update(effect_dict_curr)

with open(f'{os.path.dirname(os.path.realpath(__file__))}/effect_json/english.json', 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, ensure_ascii=False)
