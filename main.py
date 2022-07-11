import fandom_crawler
import tabletop_name_import

print("Battle Spirits card importer v0.0.2")
while True:
    print("Download card images from fandom: [D/d]")
    print("Load card names onto cards: [L/l]")
    userIn = input("Choice: ")
    cardGenerationName = input("Please input the card generation abbreviation (i.e. BSC28): ").upper()
    if userIn.lower() == "d":
        fandom_crawler.fandom_img_crawler("https://battle-spirits.fandom.com/wiki/" + cardGenerationName, cardGenerationName)
    elif userIn.lower() == "l":
        tabletop_name_import.tabletopNameImport(cardGenerationName)
    userCont = input("Continue? [(Y/y)/(N/n)]: ")
    if userCont.lower() == "n":
        break
