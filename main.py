import fandom_crawler
import tabletop_name_import

VERSION_NUM = "0.1.0"

print("Battle Spirits card importer v" + VERSION_NUM)
while True:
    print("Download card images from fandom: [D/d]")
    print("Load card names onto cards: [L/l]")
    userIn = input("Choice: ")
    if userIn.lower() != "d" and userIn.lower() != "l":
        print("Bad input, please input \"D\" or \"d\" for download, or \"L\" or \"l\" for loading without double quotes")
        continue

    cardGenerationName = input("Please input the card generation abbreviation (i.e. BSC28): ").upper()
    if userIn.lower() == "d":
        fandom_crawler.fandom_crawler("https://battle-spirits.fandom.com/wiki/" + cardGenerationName, cardGenerationName)
    elif userIn.lower() == "l":
        tabletop_name_import.tabletopNameImport(cardGenerationName)

    userCont = input("Continue? [(Y/y)/(N/n)]: ")
    if userCont.lower() == "n":
        break
