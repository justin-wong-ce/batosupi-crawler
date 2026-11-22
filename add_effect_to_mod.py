import json
from tabletop_name_import import get_description
import os

userSavesPath = os.path.expanduser("~/Documents/My Games/Tabletop Simulator/Saves/")

# Toggle languages
LANG = "ENG"      # ENG
# LANG = "CHI"      # CHI
# LANG = None         # Both


'''
Script to add card effects to a Battle Spirits mod file `BS_DEFAULT.json`.

This script will overwrite all existing cards' effects in `BS_DEFAULT.json`
to have the latest effects stored in effect_json/chinese.json or effect_json/english.json.
You will need to save your Battle Spirits tabletop save as `BS_DEFAULT.json`.
Why? Because I am lazy :)
'''

with open(f"{userSavesPath}BS_DEFAULT.json", "r", encoding="utf-8") as file:
    tt_dict = json.load(file)

for deck in tt_dict["ObjectStates"]:
    if deck["Name"] == "DeckCustom" or deck["Name"] == "Deck":
        cards_arr = deck["ContainedObjects"]
    elif deck["Name"] == "Infinite_Bag" and deck["Nickname"] != "":
        cards_arr = deck["ContainedObjects"][0]["ContainedObjects"]
    else:
        continue

    for card in cards_arr:
        nickname = card["Nickname"]
        if (card["GUID"] == "" and card["Nickname"] == "") or card["Nickname"] == "BS41-X07":
            continue

        card["Description"] = get_description(nickname, lang=LANG)
        print(card["Description"])
        print(card["Nickname"])


with open(f"{userSavesPath}BS_DEFAULT-{LANG}.json", "w", encoding="utf-8") as file:
    json.dump(tt_dict, file, ensure_ascii=False, indent=4)
