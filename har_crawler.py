import os
import re
import requests


def har_crawl():
    # Read HAR file (`./har.json`)
    urls = []
    with open("har.json") as file:
        # Extract card url (check if valid) (regex)
        for line in file:
            url = re.search(r"https:\/\/\S+card_image\/\S+.png", line)
            if url:
                urls.append(url.group(0))

    if len(urls) == 0:
        raise ValueError("No matching URLs found - please check HAR file is correct.")

    # Sort url (asc)
    urls = sorted(urls)

    # Extract card name from each url
    # Download card and save
    # Update .txt holding card names (w/ order)
    gen_name = re.search(r"BS-JA\/(\S+)\/", urls[0]).group(1).upper()
    print(f"Processing set '{gen_name}'...")

    txt_save = f"{os.path.dirname(os.path.realpath(__file__))}/decks/" + gen_name + ".txt"
    txt_print = []

    for i, url in enumerate(urls):
        print(f"{i}/{len(urls)}")
        card_name = re.search(gen_name + r"\/(\S+)\.png", url).group(1).upper()
        if "%2B" in card_name:
            card_name = card_name[:card_name.find("%2B")]
        if card_name[0].isdigit():
            card_name = "BS" + card_name
        if card_name[-1] in ["p", "P"]:
            card_name = card_name[:-1] + "-SCR"
        if card_name not in txt_print:
            txt_print.append(card_name)

        filename = "downloads/" + gen_name + "/assets/" + card_name + ".jpg"
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        try:
            with open(filename, "wb") as f:
                f.write(requests.get(url).content)
        except Exception as exception:
            print("EXCEPTION OCCURRED")
            print(exception)
            print(url, card_name, gen_name)

    with open(txt_save, "w") as txtFile:
        for i in range(len(txt_print)):
            txtFile.write(txt_print[i])
            if i < len(txt_print) - 1:
                txtFile.write("\n")
        txtFile.close()
    print(f"Done processing set {gen_name}")


# Local testing
har_crawl()
