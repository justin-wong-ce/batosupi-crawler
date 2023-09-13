import json
from tabletop_name_import import get_description
import glob
import time
import os

userSavesPath = os.path.expanduser("~/Documents/My Games/Tabletop Simulator/Saves/")

with open(f"{userSavesPath}TS_Save_13.json", "r", encoding="utf-8") as file:
    tt_dict = json.load(file)

print(tt_dict["ObjectStates"])
for deck in tt_dict["ObjectStates"]:
    if deck["Name"] != "Infinite_Bag" or deck["Nickname"] == "":
        continue
    for card in deck["ContainedObjects"][0]["ContainedObjects"]:
        nickname = card["Nickname"]
        if (card["GUID"] == "" and card["Nickname"] == "") or card["Nickname"] == "BS41-X07":
            continue

        card["Description"] = get_description(nickname)


with open(f"{userSavesPath}TS_Save_13.json", "w", encoding="utf-8") as file:
    json.dump(tt_dict, file, ensure_ascii=False, indent=4)
