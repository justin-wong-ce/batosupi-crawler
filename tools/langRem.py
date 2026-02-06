import json
import os
from tabletop_name_import import get_description

userSavesPath = os.path.expanduser("~/Documents/My Games/Tabletop Simulator/Saves/")
def keep_only_lang(lang):
    assert(lang == "CHI" or lang == "ENG")
    with open(f"{userSavesPath}BS_DEFAULT.json", "r", encoding="utf-8") as file:
        tt_dict = json.load(file)

    for deck in tt_dict["ObjectStates"]:
        # print(deck)
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

            card["Description"] = get_description(nickname, lang=lang)
            # print(card["Description"])
            # print(card["Nickname"])

    with open(f"{userSavesPath}BS_DEFAULT_{lang}.json", "w", encoding="utf-8") as file:
        json.dump(tt_dict, file, ensure_ascii=False, indent=4)

keep_only_lang("CHI")
keep_only_lang("ENG")