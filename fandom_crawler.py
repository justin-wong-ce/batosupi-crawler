import fileinput
import threading
import requests
import re
import os
import time

# JPG DL FOR FANDOM
def fandom_crawler(link, generationName):
    # Scrape link for links to individual cards
    htmlText = requests.get(link).text

    # regex pattern and parse
    pattern = re.compile(
        r"\s<td>((?:(?:BSC|BS|SD|PC|CP|TCP|TX|XX|RV|SP|CX|CB|PB|RVX)\d\d\d?(?: \([AB]\))?-?)?(?:(?:X|XX|10thX|RV|TX|TCP|CP|CX|G|XV)?\d?\d\d)?(?: \([AB]\))?)\s</td>\s<td><a href=\"([^\"]*)\"[^/]*/a>((?: \(Revival)?)")
    rows = re.findall(pattern, htmlText)

    # For each card, scrape page for png url
    txtPrint = []
    for i in range(len(rows)):
        # Wait 5 seconds for each 50 requests
        if i != 0 and i % 50 == 0:
            time.sleep(5)

        cardName = rows[i][0]
        # haveRevival = rows[i][2].find("Revival") != -1

        # BSC|BS|SD|PC|CP|TCP|TX|XX|RV
        if cardName.find("BS") == -1 and \
                cardName.find("BSC") == -1 and \
                cardName.find("SD") == -1 and \
                cardName.find("PC") == -1 and \
                cardName.find("PB") == -1 and \
                cardName.find("CB") == -1:
            # Append generation name as default
            cardName = generationName + "-" + cardName
        threading.Thread(target=fandom_scrape_png, args=(cardName, rows[i][1], generationName)).start()
        # fandom_scrape_png(cardName, rows[i][1], generationName)    # Uncomment this for single thread execution

        if cardName not in txtPrint:
            txtPrint.append(cardName)

    # Wait for threads to be done
    while True:
        if threading.active_count() == 1:
            break
    # Auto create the .txt file in decks
    txtPrint = sorted(txtPrint)
    filename = "decks/" + generationName + ".txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as txtFile:
        for i in range(len(txtPrint)):
            txtFile.write(txtPrint[i])
            if i < len(txtPrint) - 1:
                txtFile.write("\n")
        txtFile.close()

# DOM Element Remove
def filter_dom(instr):
    ret = ""
    ind = 0
    while ind < len(instr):
        # turn <br> into newlines
        if instr[ind:ind+4] == "<br>":
            ret = ret + "\n"
            ind = ind + 4
        # remove all HTML or DOM elements, effect text is never wrapped in angled brackets
        elif instr[ind] == "<":
            ind = instr[ind:].index(">") + ind + 1
        elif instr[ind:ind+4] == "&amp;":
            ret = ret + "&"
        else:
            ret = ret + instr[ind]
            ind = ind + 1
    return ret


# ENG EFFECT CRAWLER
def fandom_effect_crawler(cardName, link, generationName):
    link = "https://battle-spirits.fandom.com" + link
    htmlText = requests.get(link).text

    # regex pattern and parse
    if cardName.find("RV") != -1:
        # Fandom's revival card pages has 2 sets of card effects, need the one on the bottom
        pattern = re.compile(
            r"Kanji[\S\s]*Kanji[\S\s]*<th>Card Effects[\s]*.*[\s]*.*[\s]*(.*)[\S\s]*Card Effects \(JP/日本語\)"
        )
    else:
        pattern = re.compile(
            r"Kanji[\S\s]*<th>Card Effects[\s]*.*[\s]*.*[\s]*(.*)[\S\s]*Card Effects \(JP/日本語\)"
        )
    results = re.findall(pattern, htmlText)

    if len(results) == 0:
        # Might be due to earlier cards having different DOM layout (BS01-BS10), retry
        pattern = re.compile(
            r"Jap Version.*wds-is-current\"><p>(.*)"
        )
    results = re.findall(pattern, htmlText)
    print(filter_dom(results[0]))

    # TODO: Export to proper JSON for lua script

def fandom_scrape_png(cardName, link, generationName):
    # Use batspi for RV cards + BSC22
    if generationName == "BSC22":
        batspi_scrape_png(cardName, generationName)
    else:
        # Use fandom to get img
        link = "https://battle-spirits.fandom.com" + link
        htmlText = requests.get(link).text

        # regex pattern and parse
        if cardName.find("RV") != -1:
            pattern = re.compile(
                r"class=\"mw-headline\"[\s\S]*<a href=\"(https://static.wikia.nocookie.net/battle-spirits/images"
                r"/[^\.]*.(?:jpg|png))[\s\S]*Kanji \(漢字\)")
        else:
            pattern = re.compile(
                r"Google Tag Manager[\s\S]*<a href=\"(https://static.wikia.nocookie.net/battle-spirits/images"
                r"/[^\.]*.(?:jpg|png))[\s\S]*Kanji \(漢字\)")
        results = re.findall(pattern, htmlText)

        if len(results) == 0:
            # Might be old website format, try another regex search
            pattern = re.compile(
                r"Google Tag Manager[\s\S]*<a href=\"(https://static.wikia.nocookie.net/battle-spirits/images"
                r"/[^\.]*.(?:jpg|png)).*\s.*\s.*\s<td width=\"20%\"><b>Name")
            results = re.findall(pattern, htmlText)

        try:
            pngLink = results[0]
            # Download
            download_save(pngLink, cardName, generationName)
        except IndexError:
            print("IndexError, falling back to batspi")
            # Fallback to batspi
            batspi_scrape_png(cardName, generationName)


def download_save(image_link, name, generationName):
    filename = "downloads/" + generationName + "/assets/" + name + ".jpg"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "wb") as f:
        f.write(requests.get(image_link).content)


def batspi_scrape_png(cardName, generationName):
    batspiLink = "https://batspi.com/card/"

    # Handle TX card name brackets " (A)" to "A"
    if cardName.find(" (A)") != -1:
        cardName = cardName[:len(cardName) - 4] + "A"
    elif cardName.find(" (B)") != -1:
        cardName = cardName[:len(cardName) - 4] + "B"

    # Handle links
    if cardName.find("SD") != -1:
        batspiLink += "SD" + "/" + cardName + ".jpg"
    elif cardName.find("BSC") != -1:
        batspiLink += "BSC" + "/" + cardName + ".jpg"
    elif cardName.find("PC") != -1:
        batspiLink += "ETC" + "/" + cardName + ".jpg"
    elif cardName.find("BS") != -1:
        batspiLink += "BS" + cardName[cardName.find("BS") + 2] + "/" + cardName + ".jpg"
    else:
        currLink = "ERROR"

    download_save(batspiLink, cardName, generationName)

# Quick Tests
# fandom_scrape_png("BSC18-014", "wiki/Leona-Rikeboom#Original_", "BSC18")
# batspi_scrape_png("BS48-RV007", "BS48")
# print("\n\ntest 1: spirit - burst Alex:\n")
# fandom_scrape_png("BS52-RV007", "/wiki/The_ChosenSearcher_Alex", "BS52")
# fandom_effect_crawler("BS52-RV007", "/wiki/The_ChosenSearcher_Alex", "BS52")
# print("\n\ntest 2: magic - brave draw:\n")
# fandom_scrape_png("BS48-RV007", "/wiki/Brave_Draw", "BS48")
# fandom_effect_crawler("BS48-RV007", "/wiki/Brave_Draw", "BS48")
# print("\n\ntest 3: grandwalker nexus: mai:\n")
# fandom_scrape_png("SD51-CP01", "/wiki/Viole_Mai_-Mazoku_Side-", "SD51")
# fandom_effect_crawler("SD51-CP01", "/wiki/Viole_Mai_-Mazoku_Side-", "SD51")


# fandom_effect_crawler("BS01-X01", "/wiki/The_DragonEmperor_Siegfried", "BS01")
# fandom_scrape_png("BS01-X01", "/wiki/The_DragonEmperor_Siegfried", "BS01")
