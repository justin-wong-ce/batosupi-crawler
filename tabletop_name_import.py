import json
import os
import re
from fandom_crawler import no_effect_cards

userSavesPath = os.path.expanduser("~/Documents/My Games/Tabletop Simulator/Saves/")
try:
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/effect_json/chinese.json", "r", encoding="utf-8") as f:
        ch_dict = json.load(f)
    with open(f"{os.path.dirname(os.path.realpath(__file__))}/effect_json/english.json", "r", encoding="utf-8") as f:
        en_dict = json.load(f)
except FileNotFoundError:
    ch_dict = {}
    en_dict = {}


def get_description(nickname):
    nickname_save = nickname
    # Add chinese
    nickname = nickname.replace("\t", "") \
        .replace("10thX-", "10thX") \
        .replace("X10TH", "10thX") \
        .replace("RV-", "RV ")
    try:
        try:
            description = ch_dict[nickname]
        except KeyError:
            try:
                description = ch_dict[nickname.replace("-", "")]
            except KeyError:
                try:
                    nickname = nickname.split("-")
                    description = ch_dict[nickname[0] + "-" + nickname[1].zfill(3)]
                except KeyError:
                    print("KeyError on card (ch): " + nickname_save)
                    description = "[CHINESE] Missing - new cards may not have translations yet\n" \
                        + "If this is an old card, let us know!"
    except:
        print("FATAL PARSE ERROR")
        description = "[CHI] FATAL ERROR\n"

    # Add english
    nickname = nickname_save
    nickname = nickname.replace("\t", "") \
        .replace("10thX-", "10thX") \
        .replace("X10TH", "10thX") \
        .replace("RV-", "RV") \
        .replace("RV  ", "RV") \
        .replace("RV ", "RV") \
        .replace("EX-", "EX") \
        .replace("(A)", " (A)") \
        .replace("(B)", " (B)") \
        .replace("LM18-G06", "LM18-G06-X")
    if re.search(r"^BS4\d-\d{2}$", nickname):
        nickname = nickname.replace("-", "-0")

    if nickname in no_effect_cards:
        return ""
    try:
        if en_dict[nickname] == "-" or en_dict[nickname] == "":
            return
    except KeyError:
        if nickname in missing_effects:
            description = description + "\n\n" + missing_effects[nickname] + "\n(Translation by nepuUbU)"
            return description
    try:
        description = description + "\n\n" + en_dict[nickname] + "\n(Translation from Fandom Wiki)"
    except KeyError:
        try:
            description = description + "\n\n" + \
                          en_dict[nickname.replace("-", "")] + "\n(Translation from Fandom Wiki)"
        except KeyError:
            print("KeyError on card (en): " + nickname_save + ", post edit: " + nickname)
            description = description + "\n\n[ENGLISH] Bad - let us know! (new cards may not have translations yet)"
    description = description.replace("&amp;", "&").replace("()", "")
    return description


def tabletop_name_import(deck_name):
    # Edits Tabletop Save file to import names
    f1 = open(userSavesPath + "TS_Save_-.json", "r", encoding="utf-8")
    deck_folder = "decks"
    json_contents = f1.read()
    f1.close()

    decks_to_rename = [deck_name]

    save_object = json.loads(json_contents)
    object_states = save_object["ObjectStates"]
    decks = [object_state
             for object_state in object_states
             if object_state["Name"] == "DeckCustom" or object_state["Name"] == "Deck"
             and object_state["Nickname"]
             in decks_to_rename]

    deck_files = {}
    for deck_nickname in decks_to_rename:
        file_name = deck_nickname.replace(" ", "-") + ".txt"
        f2 = open(deck_folder + "/" + file_name, "r", encoding="utf-8")
        deck_files[deck_nickname] = f2

    for deck in decks:
        nickname = deck["Nickname"]
        if nickname != deck_name:
            continue
        deck_file = deck_files[nickname]
        file_content = deck_file.read()
        print(file_content)
        file_lines = file_content.split("\n")

        cards = deck["ContainedObjects"]

        print("file_lines: {}, cards: {}".format(len(file_lines), len(cards)))
        assert len(cards) == len(file_lines)

        for i in range(len(cards)):
            cards[i]["Nickname"] = file_lines[i]
            card_nickname = cards[i]["Nickname"]
            if cards[i]['Nickname'] == 'BS41-X07':
                continue

            cards[i]["Description"] = get_description(card_nickname)
        new_savefile_contents = json.dumps(save_object, indent=2)

    wf = open(userSavesPath + "TS_Save_-.json", "w", encoding="utf-8")
    wf.write(new_savefile_contents)
    wf.close()
    print("Imported")


missing_effects = {
    "BS01-093": "[LV1][LV2] (When Attacks)\nWhen you opponent declares a block, "
                "exhaust one of your opponent\'s Spirit except the blocking Spirit.\n"
                "[LV2] (When Destroyed)\nRefresh one of your Spirits.",
    "BS03-093": "[LV1][LV2][LV3] (When Attacks)\nThis Spirit gains +2000 BP.",
    "BS04-093": "Flash - During this term, all opponent's Spirits cannot activate their (When Destroyed) effect.",
    "BS40-CP04": "Flash - Advent: Cost 5 or more  (Either Attack Step)\nBy sending your  to the Trash, "
                 "stack this from your hand onto your target Spirit.\n\n"
                 "[LV1][LV2][LV3] (When Advents)\n"
                 "Draw one card from your deck, and during this turn, this Spirit gains +10000 BP.\n"
                 "[LV2][LV3] (When destroyed)\n"
                 "By discarding one of this Spirit's Pre-Advent cards, "
                 "this Spirit can remain on the field in refresh state.",
    "BS40-CP05": "Flash - Advent: Cost 5 or more  (Either Attack Step)\nBy sending your  to the Trash, "
                 "stack this from your hand onto your target Spirit.\n\n"
                 "[LV1][LV2][LV3] (When Advents)\n"
                 "Draw one card from your deck, and during this turn, this Spirit gains +10000 BP.\n"
                 "[LV2][LV3] (When destroyed)\n"
                 "By discarding one of this Spirit's Pre-Advent cards, "
                 "this Spirit can remain on the field in refresh state.",
    "BS40-CP06": "Flash - Advent: Cost 5 or more  (Either Attack Step)\nBy sending your  to the Trash, "
                 "stack this from your hand onto your target Spirit.\n\n"
                 "[LV1][LV2][LV3] (When Advents)\n"
                 "Draw one card from your deck, and during this turn, this Spirit gains +10000 BP.\n"
                 "[LV2][LV3] (When destroyed)\n"
                 "By discarding one of this Spirit's Pre-Advent cards, "
                 "this Spirit can remain on the field in refresh state.",
    "BS40-CP07": "Flash - Advent: Cost 5 or more  (Either Attack Step)\nBy sending your  to the Trash, "
                 "stack this from your hand onto your target Spirit.\n\n"
                 "[LV1][LV2][LV3] (When Advents)\n"
                 "Draw one card from your deck, and during this turn, this Spirit gains +10000 BP.\n"
                 "[LV2][LV3] (When destroyed)\n"
                 "By discarding one of this Spirit's Pre-Advent cards, "
                 "this Spirit can remain on the field in refresh state.",
    "BS40-CP08": "Flash - Advent: Cost 5 or more  (Either Attack Step)\nBy sending your  to the Trash, "
                 "stack this from your hand onto your target Spirit.\n\n"
                 "[LV1][LV2][LV3] (When Advents)\n"
                 "Draw one card from your deck, and during this turn, this Spirit gains +10000 BP.\n"
                 "[LV2][LV3] (When destroyed)\n"
                 "By discarding one of this Spirit's Pre-Advent cards, "
                 "this Spirit can remain on the field in refresh state.",
    "BS40-CP09": "Flash - Advent: Cost 5 or more  (Either Attack Step)\nBy sending your  to the Trash, "
                 "stack this from your hand onto your target Spirit.\n\n"
                 "[LV1][LV2][LV3] (When Advents)\n"
                 "Draw one card from your deck, and during this turn, this Spirit gains +10000 BP.\n"
                 "[LV2][LV3] (When destroyed)\n"
                 "By discarding one of this Spirit's Pre-Advent cards, "
                 "this Spirit can remain on the field in refresh state."
}
