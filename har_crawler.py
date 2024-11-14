import os
import re
import requests
import threading
import time

THREADING_ON = True

def download_image(url, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    try:
        with open(filepath, "wb") as f:
            f.write(requests.get(url).content)
    except Exception as exception:
        print("EXCEPTION OCCURRED")
        print(exception)
        print(url, filepath)

def har_crawl():
    # Read HAR file (`./har.json`)
    urls = []
    with open("har.json") as file:
        # Extract card url (check if valid) (regex)
        for line in file:
            url = re.search(r"https:\/\/\S+card_image\/\S+.(?:png|jpg|PNG|JPG)", line)
            if url:
                urls.append(url.group(0))

    if len(urls) == 0:
        raise ValueError("No matching URLs found - please check HAR file is correct.")

    # Sort url (asc)
    urls = sorted(urls)

    # Extract card name from each url
    # Download card and save
    # Update .txt holding card names (w/ order)
    gen_name = re.search(r"card_image\/BS-JA\/(\S+)\/", urls[0]).group(1).upper()
    print(f"Processing set '{gen_name}'...")

    txt_save = f"{os.path.dirname(os.path.realpath(__file__))}/decks/" + gen_name + ".txt"
    txt_print = []

    threads = []
    for i, url in enumerate(urls):
        try:
            card_name = re.search(r"card_image\/BS-JA\/\S+\/(\S+)\.(?:png|jpg|PNG|JPG)", url).group(1).upper()
        except AttributeError as err:
            print(f"ERR card_name parse - cannot parse name from url: {url}, gen_name: {gen_name}")
            raise AttributeError(err)
        if "%2B" in card_name:
            card_name = card_name[:card_name.find("%2B")]
        if "-" not in card_name:
            card_name = f"{gen_name}-{card_name}"
        if card_name[0].isdigit():
            card_name = "BS" + card_name
        card_name = card_name.replace("_", "-")
        if card_name[-2:] in ["-D", "-d"]:
            card_name = card_name[:-2]
        if card_name[-1] in ["P", "p"]:
            card_name = card_name[:-1] + "-SCR"

        if card_name not in txt_print:
            txt_print.append(card_name)

        filename = "downloads/" + gen_name + "/assets/" + card_name + ".jpg"

        if THREADING_ON:
            threads.append(threading.Thread(target=download_image, args=(url, filename)))
            threads[i].start()
            if len(threads) % 40 == 1:
                time.sleep(2)
            print(f"Threads launched: {i}/{len(urls)}")
        else:
            print(f"{i}/{len(urls)}")
            download_image(url, filename)

    count = 0
    while True and THREADING_ON:
        active_threads = threading.active_count()
        if active_threads == 1:
            print(f"Threads done: {len(urls)}/{len(urls)}")
            break
        elif active_threads != count:
            count = active_threads
            print(f"Threads done: {len(urls) - count}/{len(urls)}")
        time.sleep(0.1)

    with open(txt_save, "w") as txtFile:
        txt_print.sort()
        for i in range(len(txt_print)):
            txtFile.write(txt_print[i])
            if i < len(txt_print) - 1:
                txtFile.write("\n")
        txtFile.close()
    print(f"Done processing set {gen_name}")


# Local testing
har_crawl()
