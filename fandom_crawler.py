import threading
import requests
import re
import os


# JPG DL FOR FANDOM
def fandom_img_crawler(link, generationName):
    # Scrape link for links to individual cards
    htmlText = requests.get(link).text

    # regex pattern and parse
    pattern = re.compile(
        r"\s<td>((?:(?:BSC|BS|SD|PC|CP|TCP|TX|XX|RV|SP|CX)\d\d\d?(?: \([AB]\))?-?)?(?:(?:X|XX|10thX|RV|TX|TCP|CP|CX)?\d?\d\d)?)\s</td>\s<td><a href=\"([^\"]*)\"")
    rows = re.findall(pattern, htmlText)

    # For each card, scrape page for png url
    txtPrint = []
    for i in range(len(rows)):
        cardName = rows[i][0]
        # BSC|BS|SD|PC|CP|TCP|TX|XX|RV
        if cardName.find("BS") == -1 and \
                cardName.find("BSC") == -1 and \
                cardName.find("SD") == -1 and \
                cardName.find("PC") == -1 and \
                cardName.find("CP") == -1:
            # Append generation name as default
            cardName = generationName + "-" + cardName

        threading.Thread(target=fandom_scrape_png, args=(cardName, rows[i][1], generationName)).start()
        # fandom_scrape_png(cardName, rows[i][1]) # Uncomment this for single thread execution

        txtPrint.append(cardName)

    # Wait for threads to be done
    while True:
        if threading.active_count() == 1:
            break
    # Generate dump to stdout to copy to txt, for use with tabletop_name_import.py
    # TODO: Auto create the .txt file in decks
    filename = "decks/" + generationName + ".txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as txtFile:
        for card in txtPrint:
            txtFile.write(card + "\n")


def fandom_scrape_png(cardName, link, generationName):
    # Use batspi for RV cards
    if cardName.find("RV") != -1:
        batspi_scrape_png(cardName, generationName)
    else:
        # Use fandom to get img
        link = "https://battle-spirits.fandom.com" + link
        htmlText = requests.get(link).text

        # regex pattern and parse
        pattern = re.compile(
            r"<meta property=\"og:image\" content=\"(https://static.wikia.nocookie.net/battle-spirits/images/[^\"]*.(?:jpg|png))")
        results = re.findall(pattern, htmlText)

        try:
            pngLink = results[0]
            # download
            download_save(pngLink, cardName, generationName)
        except IndexError:
            # fallback to batspi
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


# fandom_scrape_png("BSC18-014", "wiki/Leona-Rikeboom#Original_")
# batspi_scrape_png("BS48-RV007", "BS48")
