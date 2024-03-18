import json
from tabletop_name_import import get_description
import os

userSavesPath = os.path.expanduser("~/Documents/My Games/Tabletop Simulator/Saves/")

with open(f"{userSavesPath}TS_Save_13.json", "r", encoding="utf-8") as file:
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

        card["Description"] = get_description(nickname)
        print(card["Description"])
        print(card["Nickname"])


with open(f"{userSavesPath}TS_Save_13.json", "w", encoding="utf-8") as file:
    json.dump(tt_dict, file, ensure_ascii=False, indent=4)
