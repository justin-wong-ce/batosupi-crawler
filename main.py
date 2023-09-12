import fandom_crawler
import tabletop_name_import

VERSION_NUM = "0.1.0"

print("Battle Spirits card importer v" + VERSION_NUM)
while True:
    print("Download card images: [D/d]")
    print("Scrape card effects: [S/s]")
    print("Load card names onto cards: [L/l]")
    userIn = input("Choice: ")
    if userIn.lower() != "d" and userIn.lower() != "l" and userIn.lower() != "s":
        print("Bad input, please input:\n"
              "\"D\" or \"d\" for download, or\n"
              "\"S\" or \"s\" for scraping card effects, or\n"
              "\"L\" or \"l\" for loading without double quotes")
        continue

    cardGenerationName = input("Please input the card generation abbreviation (i.e. BSC28): ").upper()
    if userIn.lower() == "d":
        fandom_crawler.fandom_crawler("https://battle-spirits.fandom.com/wiki/" + cardGenerationName,
                                      cardGenerationName, True)
    elif userIn.lower() == "l":
        tabletop_name_import.tabletopNameImport(cardGenerationName)
    else:
        fandom_crawler.fandom_crawler("https://battle-spirits.fandom.com/wiki/" + cardGenerationName,
                                      cardGenerationName, False)

    userCont = input("Continue? [(Y/y)/(N/n)]: ")
    if userCont.lower() == "n":
        break
