import fandom_crawler
import threading
import requests
import re
import os
import json

""" 
Special crawler just for Promo cards due to high complexity of Promo Cards page

Challenge: 
- Page itself contains links to cards, but also sets
- Some card names are missing prefix (old Promo cards i.e.Promo 12)
- Weird prefixes (KFC, GX, etc.)

I could've written a more robust version and integrated into main crawler, but seems too much work
"""
IMG_MODE = False        # True: scrape images; False: scrape effects
# IMG_MODE not implemented

effect_dict = {}
html_text = requests.get("https://battle-spirits.fandom.com/wiki/Promo_Cards").text

# Acquire section names first
pattern = re.compile(
    r"toclevel-1 tocsection-\d\d?\"><a href=\"#([^\"^\n^\r]*)"
)

sections = re.findall(pattern, html_text)

# Get cards
pattern = re.compile(
    r"<td>((?:(?:(?:P|CP|SD|BS|PX|X|GX)?\d\d\d?|BSH)(?: \([AB]\))?-?)"
    r"(?:(?:X|CP|PX|EX)?\d?\d\d[RAEDTS]?)?(?: \([AB]\))?)\s</td>\s<td><a href=\"([^\"]*)"
)
cards = re.findall(pattern, html_text)
for i in range(len(cards)):
    # card format: [CARD NAME, /wiki LINK TO CARD]
    card_list = list(cards[i])
    if re.search(r"^\d{3}$", card_list[0]):
        # Append "P" to card names for regular promos
        card_list[0] = "P" + card_list[0]
    elif re.search(r"^\d{2}-\d{2}[RAEDTS]?(?: \([AB]\))?$", card_list[0]):
        # Append "P" to card names for Promo XX
        card_list[0] = "P" + card_list[0]
    cards[i] = tuple(card_list)


# Section does not contain cards, instead a link to wiki
# [SECTION NAME, /wiki LINK TO CARD SET]
links = []
pattern = re.compile("class=\"mw-headline\" id=\"(?=(" + "|".join(sections) +
                     r")).*\s*(?:.*\s*)?(?:<ul><li>|<p>)<a href=\"([^\"]*)")
links.extend(re.findall(pattern, html_text))
pattern = re.compile("class=\"mw-headline\" id=\"(?=(" + "|".join(sections) +
                     r")).*\s*(?:.*\s*)?<li><a href=\"([^\"]*)")
links.extend(re.findall(pattern, html_text))
links = set(links)

count = 0
for card in cards:
    # threading.Thread(target=fandom_crawler.fandom_scrape_effect, args=(card[0], card[1], effect_dict))
    fandom_crawler.fandom_scrape_effect(card[0], card[1], effect_dict)
    count = count + 1
    if count % 100 == 0:
        print("100 Promo cards processed")

for link in links:
    fandom_crawler.fandom_crawler("https://battle-spirits.fandom.com" + link[1], link[0], False, True)
    print("Processing: " + link[1])

# Adding normal ones too, one time
for i in range(1, 66):
    print("Processing: BS" + f"{i:02d}")
    fandom_crawler.fandom_crawler("https://battle-spirits.fandom.com/wiki/BS" + f"{i:02d}", "BS" + f"{i:02d}",
                                  False, False)
for i in range(1, 67):
    print("Processing: SD" + f"{i:02d}")
    fandom_crawler.fandom_crawler("https://battle-spirits.fandom.com/wiki/SD" + f"{i:02d}", "SD" + f"{i:02d}",
                                  False, False)
for i in range(1, 43):
    print("Processing: BSC" + f"{i:02d}")
    fandom_crawler.fandom_crawler("https://battle-spirits.fandom.com/wiki/BSC" + f"{i:02d}", "BSC" + f"{i:02d}",
                                  False, False)
for i in range(1, 29):
    print("Processing: CB" + f"{i:02d}")
    fandom_crawler.fandom_crawler("https://battle-spirits.fandom.com/wiki/CB" + f"{i:02d}", "CB" + f"{i:02d}",
                                  False, False)

# Wait for threads to be done
# while True:
#     if threading.active_count() == 1:
#         break

try:
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/effect_json/english.json", "r", encoding='utf-8') as f:
        effect_dict_curr = json.load(f)
except FileNotFoundError:
    print("File not found")
    pass

effect_dict.update(effect_dict_curr)

with open(f'{os.path.dirname(os.path.realpath(__file__))}/effect_json/english.json', 'w', encoding='utf-8') as f:
    json.dump(effect_dict, f, ensure_ascii=False)