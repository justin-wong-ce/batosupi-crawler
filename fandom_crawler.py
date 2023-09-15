import threading
import requests
import re
import os
import time
import json


# JPG DL FOR FANDOM
def fandom_crawler(link, gen_name, is_img_dl, no_name_tamper, effect_threading, effect_dict):
    if not is_img_dl and not effect_threading:
        effect_dict = {}

    # Scrape link for links to individual cards
    try:
        html_text = requests.get(link).text
    except:
        print("bad link")
        return

    # regex pattern and parse
    pattern = re.compile(
        r"\s<td>((?:(?:(?:(?:(?:BSC|BS|SD|PC|CP|GX|TCP|TX|XX|RV|SP|CX|CB|PB|RVX|KF|LM|SJ|PX|P)\d\d\d?|KF)(?: \([AB]\))?-?)?(?:("
        r"?:X|XX|10thX|RV|RVX|RVXX|TX|TCP|CP|CX|G|XV|U|D|H|SP|A|XA|XXA|DD)?\d?\d\d)(?:\s?\([AB]\))?(?:-X)?)|(?:\d\d-EXG\d\d)))\s*</td>\s*<td><a [^>]*href=\""
        r"([^\"]*)\".*/a>")
    rows = re.findall(pattern, html_text)

    # For each card, scrape page for png url
    txt_print = []
    threads = []
    for i in range(len(rows)):
        url = rows[i][1]
        if url.find("https") != -1:
            url = url[url.find("/wiki"):]

        # Wait 1 seconds for each 50 requests
        if i != 0 and i % 50 == 0:
            time.sleep(1)

        card_name = rows[i][0]
        if re.search(r"\d\((?:A|B)\)", card_name):
            card_name = card_name.replace("(", " (")

        if re.search(r"^SD3[789]$", gen_name) and card_name.find("006") != -1:
            card_name = card_name.replace("SD36", gen_name)
        elif card_name == "SD38-012" and url.find("Binding") != -1:
            card_name = "SD38-014"
        elif re.search(r"^CB0[467]$", gen_name) and card_name.find("038") != -1:
            card_name = card_name.replace("CB02", gen_name)
        elif gen_name == "BSC24" and card_name == "BSC23-036":
            card_name = "BSC24-036"
        elif gen_name == "BSC23" and card_name == "BSC18-041":
            card_name = "BSC23-041"

        if re.search(r"^[^-]+$", card_name) and no_name_tamper is False:
            # Append generation name as default
            card_name = gen_name + "-" + card_name
        if is_img_dl:
            threads.append(threading.Thread(target=fandom_scrape_png, args=(card_name, url, gen_name)))
        else:
            threads.append(threading.Thread(target=fandom_scrape_effect, args=(card_name, url, effect_dict)))
        threads[i].start()

        if card_name not in txt_print:
            txt_print.append(card_name)

    # Wait for threads to be done
    for thread in threads:
        thread.join()
    
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
    elif not effect_threading:
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
            json.dump(effect_dict_curr, f, ensure_ascii=False)


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

    if card_name in no_effect_cards:
        effect_dict.update({card_name: ""})
        return

    if card_name.find("RV") != -1:
        try:
            results[0] = results[1]
        except:
            pass

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
        if re.search(r"^17-EXG\d{2}$", card_name):
            card_name = "P" + card_name
            print("Changing EXG")
        elif re.search(r"^\d{3}$", card_name) or \
                re.search(r"^\d{2}-\d{2}[RAEDTS]?(?: \([AB]\))?$", card_name) or \
                re.search(r"^17-EXG\d{2}", card_name):
            card_name = "P" + card_name
        elif re.search(r"^X-\d{3}[RAEDTS]?$", card_name):
            card_name = card_name.replace("X-", "X")
        elif re.search(r"^PX-\d{2}$", card_name):
            card_name = card_name.replace("PX-", "PX19-")
        elif card_name == "CP17-X07":
            card_name = "CP14-X07"
        effect_dict.update({card_name: filter_dom(results[0])})

    except IndexError:
        effect_dict.update({card_name: "-"})
        if card_name not in no_effect_cards:
            print("NO EFFECT FOUND: " + card_name)


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


no_effect_cards = {
    "SJ13-10",
    "SJ13-11",
    "SJ13-13",
    "SJ13-14",
    "SJ13-15",
    "SJ13-19",
    "BS02-051",
    "BS02-053",
    "BS03-020",
    "BS03-041",
    "BS03-071",
    "BS03-072",
    "BS04-040",
    "BS05-045",
    "BS10-004",
    "BS10-028",
    "BS16-028",
    "BS19-063",
    "BS20-046",
    "BS31-057",
    "BS32-050",
    "BS33-005",
    "BS33-012",
    "BS35-006",
    "BS35-017",
    "BS35-032",
    "BS35-034",
    "BS35-048",
    "BS35-061",
    "BS36-006",
    "BS36-019",
    "BS36-025",
    "BS36-035",
    "BS36-042",
    "BS36-048",
    "BS37-008",
    "BS37-019",
    "BS37-024",
    "BS37-048",
    "BS37-067",
    "BS40-001",
    "BS44-049",
    "BS46-015",
    "BS50-RV006",
    "SD01-022",
    "BS03-071",
    "BS03-072",
    "SD20-001",
    "SD22-001",
    "SD33-004",
    "SD34-006",
    "BSC19-003",
    "BSC19-006",
    "BSC19-018",
    "BSC19-020",
    "BSC24-002",
    "BSC26-001",
    "BSC26-013",
    "BSC26-020",
    "BSC26-024",
    "BSC26-032",
    "BSC26-038",
    "BS37-048",
    "BSC42-003",
    "BSC42-013",
    "BSC42-032",
    "BSC42-047",
    "BSC42-056",
    "BSC42-070",
    "CB01-001",
    "CB01-004",
    "CB01-017",
    "CB01-035",
}

# Quick Tests
# effect_test = {}
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

# fandom_scrape_effect("BS56-058", "/wiki/The_SpacePirateOperator_Lisitsa", effect_test)
# fandom_scrape_effect("dfg", "/wiki/Atomic_Breath", effect_test)
# print(effect_test)

