import threading
import requests
import re
import os
import time
import json


# JPG DL FOR FANDOM
def fandom_crawler(link, gen_name, is_img_dl, no_name_tamper):
    if not is_img_dl:
        effect_dict = {}

    # Scrape link for links to individual cards
    try:
        html_text = requests.get(link).text
    except:
        print("bad link")
        return

    # regex pattern and parse
    pattern = re.compile(
        r"\s<td>((?:(?:(?:(?:(?:BSC|BS|SD|PC|CP|TCP|TX|XX|RV|SP|CX|CB|PB|RVX|KF|LM|SJ|PX|P)\d\d\d?|KF)(?: \([AB]\))?-?)?(?:("
        r"?:X|XX|10thX|RV|TX|TCP|CP|CX|G|XV|U|D)?\d?\d\d)(?: \([AB]\))?(?:-X)?)|(?:\d\d-EXG\d\d)))\s</td>\s<td><a href=\""
        r"([^\"]*)\"[^/]*/a>((?: \(Revival)?)")
    rows = re.findall(pattern, html_text)

    # For each card, scrape page for png url
    txt_print = []
    for i in range(len(rows)):
        # Wait 1 seconds for each 50 requests
        if i != 0 and i % 50 == 0:
            time.sleep(1)

        card_name = rows[i][0]
        # haveRevival = rows[i][2].find("Revival") != -1

        if card_name.find("BS") == -1 and \
                card_name.find("BSC") == -1 and \
                card_name.find("SD") == -1 and \
                card_name.find("PC") == -1 and \
                card_name.find("PB") == -1 and \
                card_name.find("CB") == -1 and \
                no_name_tamper is False:
            # Append generation name as default
            card_name = gen_name + "-" + card_name
        if is_img_dl:
            threading.Thread(target=fandom_scrape_png, args=(card_name, rows[i][1], gen_name)).start()
        else:
            # threading.Thread(target=fandom_scrape_effect, args=(card_name, rows[i][1], effect_dict)).start()
            fandom_scrape_effect(card_name, rows[i][1], effect_dict)

        if card_name not in txt_print:
            txt_print.append(card_name)

    # Wait for threads to be done
    while True:
        if threading.active_count() == 1:
            break
    
    if is_img_dl:
        # Auto create the .txt file in decks
        txt_print = sorted(txt_print)
        filename = f"{os.path.dirname(os.path.realpath(__file__))}/decks/" + gen_name + ".txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w") as txtFile:
            for i in range(len(txt_print)):
                txtFile.write(txt_print[i])
                if i < len(txt_print) - 1:
                    txtFile.write("\n")
            txtFile.close()
    else:
        try:
            with open(f"{os.path.dirname(os.path.realpath(__file__))}/effect_json/english.json",
                      "r", encoding="utf-8") as f:
                effect_dict_curr = json.load(f)
        except FileNotFoundError:
            print("File not found")
            effect_dict_curr = {}
            pass
        # Create the effects .json
        effect_dict_curr.update(effect_dict)
        with open(f"{os.path.dirname(os.path.realpath(__file__))}/effect_json/english.json", "w", encoding="utf-8") as f:
            json.dump(effect_dict, f, ensure_ascii=False)


# DOM Element Remove
def filter_dom(instr):
    ret = ""
    ind = 0
    after_newline = True
    while ind < len(instr):
        # turn <br> and </div> into newlines
        if instr[ind:ind+4] == "<br>":
            ret = ret + "\n"
            ind = ind + 4
            after_newline = True
        elif instr[ind:ind+6] == "</div>":
            ret = ret + "\n"
            ind = ind + 6
            after_newline = True
        # remove all HTML or DOM elements, effect text is never wrapped in angled brackets
        elif instr[ind] == "<":
            ind = instr[ind:].index(">") + ind + 1
        elif instr[ind:ind+4] == "&amp;":
            ret = ret + "&"
        elif after_newline is True:
            if instr[ind] != " ":
                ret = ret + instr[ind]
                after_newline = False
            ind = ind + 1
        else:
            ret = ret + instr[ind]
            ind = ind + 1
    return ret

# Backup regex, add more as bugs occur
reg_str = [
    r"Jap Version.*wds-is-current\"><p>(.*)",
    r"<i>English</i>\s*.*\s*.*\s*.*wds-is-current\"><p>(.*)",
    r"<i>English</i>\s*.*\s*.*\s*(.*)",
]


# ENG EFFECT CRAWLER
def fandom_scrape_effect(card_name, link, effect_dict):
    link = "https://battle-spirits.fandom.com" + link
    html_text = requests.get(link).text

    # regex pattern and parse
    pattern = re.compile(
        r"<th>Card Effects\n.*[\s]*.*[\s]*(.*)"
    )
    results = re.findall(pattern, html_text)

    if card_name.find("RV") != -1:
        results[0] = results[1]

    ind = 0
    while len(results) == 0 and ind < len(reg_str):
        # Might be due to earlier cards having different DOM layout, retry
        pattern = re.compile(
            reg_str[ind]
        )
        results = re.findall(pattern, html_text)
        ind = ind + 1

    try:
        if results[0].find("{effect}") != -1:
            results[0] = ""
        # print(filter_dom(results[0]))
        # if results[0] == "":
        #     print(card_name + "NO EFFECT")
        effect_dict.update({card_name: filter_dom(results[0])})

    except IndexError:
        # print("COULD NOT FIND EFFECT - " + card_name)
        effect_dict.update({card_name: "-"})


def fandom_scrape_png(card_name, link, gen_name):
    # Use batspi for RV cards + BSC22
    if gen_name == "BSC22":
        batspi_scrape_png(card_name, gen_name)
    else:
        # Use fandom to get img
        link = "https://battle-spirits.fandom.com" + link
        html_text = requests.get(link).text

        # regex pattern and parse
        if card_name.find("RV") != -1:
            pattern = re.compile(
                r"class=\"mw-headline\"[\s\S]*<a href=\"(https://static.wikia.nocookie.net/battle-spirits/images"
                r"/[^\.]*.(?:jpg|png))[\s\S]*Card Type")
        else:
            pattern = re.compile(
                r"Google Tag Manager[\s\S]*<a href=\"(https://static.wikia.nocookie.net/battle-spirits/images"
                r"/[^\.]*.(?:jpg|png))[\s\S]*Card Type")
        results = re.findall(pattern, html_text)

        if len(results) == 0:
            # Might be old website format, try another regex search
            pattern = re.compile(
                r"Google Tag Manager[\s\S]*<a href=\"(https://static.wikia.nocookie.net/battle-spirits/images"
                r"/[^\.]*.(?:jpg|png)).*\s.*\s.*\s<td width=\"20%\"><b>Name")
            results = re.findall(pattern, html_text)

        try:
            png_url = results[0]
            # Download
            download_save(png_url, card_name, gen_name)
        except IndexError:
            print("IndexError, falling back to batspi")
            # Fallback to batspi
            batspi_scrape_png(card_name, gen_name)


def download_save(image_link, name, gen_name):
    filename = "downloads/" + gen_name + "/assets/" + name + ".jpg"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        f.write(requests.get(image_link).content)


def batspi_scrape_png(card_name, gen_name):
    batspi_url = "https://batspi.com/card/"

    # Handle TX card name brackets " (A)" to "A"
    if card_name.find(" (A)") != -1:
        card_name = card_name[:len(card_name) - 4] + "A"
    elif card_name.find(" (B)") != -1:
        card_name = card_name[:len(card_name) - 4] + "B"

    # Handle links
    if card_name.find("SD") != -1:
        batspi_url += "SD" + "/" + card_name + ".jpg"
    elif card_name.find("BSC") != -1:
        batspi_url += "BSC" + "/" + card_name + ".jpg"
    elif card_name.find("PC") != -1:
        batspi_url += "ETC" + "/" + card_name + ".jpg"
    elif card_name.find("BS") != -1:
        batspi_url += "BS" + card_name[card_name.find("BS") + 2] + "/" + card_name + ".jpg"
    else:
        batspi_url = "ERROR"

    download_save(batspi_url, card_name, gen_name)

# Quick Tests
effect_test = {}
# fandom_scrape_png("BSC18-014", "wiki/Leona-Rikeboom#Original_", "BSC18")
# batspi_scrape_png("BS48-RV007", "BS48")

# print("\n\ntest 1: spirit - burst Alex:\n")
# fandom_scrape_png("BS52-RV007", "/wiki/The_ChosenSearcher_Alex", "BS52")
# fandom_scrape_effect("BS52-RV007", "/wiki/The_ChosenSearcher_Alex")
# print("\n\ntest 2: magic - brave draw:\n")
# fandom_scrape_png("BS48-RV007", "/wiki/Brave_Draw", "BS48")
# fandom_scrape_effect("BS48-RV007", "/wiki/Brave_Draw", effect_test)
# print("\n\ntest 3: grandwalker nexus: mai:\n")
# fandom_scrape_png("SD51-CP01", "/wiki/Viole_Mai_-Mazoku_Side-", "SD51")
# fandom_scrape_effect("SD51-CP01", "/wiki/Viole_Mai_-Mazoku_Side-")
# print("\n\ntest 4: mirage spirit: begasusmachinebeast pegaspace:\n")
# fandom_scrape_png("BS59-031", "/wiki/The_PegasusMachineBeast_Pegaspace", "BS59")
# fandom_scrape_effect("BS59-031", "/wiki/The_PegasusMachineBeast_Pegaspace")

# # old website test
# fandom_scrape_effect("BS01-X01", "/wiki/The_DragonEmperor_Siegfried")
# fandom_scrape_png("BS01-X01", "/wiki/The_DragonEmperor_Siegfried", "BS01")
# fandom_scrape_effect("BS01-041", "/wiki/Cobraiga")
# fandom_scrape_effect("BS01-138", "/wiki/Hand_Reverse")

fandom_scrape_effect("BS56-058", "/wiki/The_SpacePirateOperator_Lisitsa", effect_test)
fandom_scrape_effect("BS56-TX03 (B)", "/wiki/The_DragonKnightEmperor_Grand-Dragonic-Arthur", effect_test)
print(effect_test)

