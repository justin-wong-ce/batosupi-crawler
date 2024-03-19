import fandom_crawler
import tabletop_name_import
import chinese_effect_crawler

VERSION_NUM = "0.2.0"

print("Battle Spirits card importer v" + VERSION_NUM)
while True:
    print("Download card images: [D/d]")
    print("Scrape card effects: [S/s]")
    print("Load card names onto cards: [L/l]")
    user_in = input("Choice: ")
    if user_in.lower() != "d" and user_in.lower() != "l" and user_in.lower() != "s":
        print("Bad input, please input:\n"
              "\"D\" or \"d\" for download, or\n"
              "\"S\" or \"s\" for scraping card effects, or\n"
              "\"L\" or \"l\" for loading without double quotes")
        continue

    card_gen_name = input("Please input the card generation abbreviation (i.e. BSC28): ")
    if user_in.lower() == "d":
        url = input("Page link (LEAVE EMPTY TO AUTO GENERATE): ")
        url = url or "https://battle-spirits.fandom.com/wiki/" + card_gen_name
        fandom_crawler.fandom_crawler(url, card_gen_name, True, False, False, None)
    elif user_in.lower() == "l":
        tabletop_name_import.tabletop_name_import(card_gen_name)
    elif user_in.lower() == "s":
        print("Scraping English effects...")
        fandom_crawler.fandom_crawler("https://battle-spirits.fandom.com/wiki/" + card_gen_name,
                                      card_gen_name, False, False, False, None)
        print("DONE\nScraping Chinese effects...")
        chinese_effect_crawler.scrape_chinese_effect(card_gen_name)
        print("DONE")

    userCont = input("Continue? [(Y/y)/(N/n)]: ")
    if userCont.lower() == "n":
        break
