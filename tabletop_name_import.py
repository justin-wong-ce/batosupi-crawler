import json
import os

userSavesPath = os.path.expanduser("~/Documents/My Games/Tabletop Simulator/Saves/")
with open(f'{os.path.dirname(os.path.realpath(__file__))}/effect_json/chinese.json', 'r', encoding='utf-8') as f:
    card_effect = json.load(f)

def tabletopNameImport(deckName):
    # Edits Tabletop Save file to import names
    f = open(userSavesPath + "TS_Save_0.json", "r")
    deck_folder = "decks"
    json_contents = f.read()
    f.close()

    decks_to_rename = [deckName]

    save_object = json.loads(json_contents)
    object_states = save_object["ObjectStates"]
    decks = [object_state
             for object_state in object_states
             if object_state["Name"] == "DeckCustom"
             and object_state["Nickname"]
             in decks_to_rename]
    print(decks)
    deck_files = {}
    for deck_nickname in decks_to_rename:
        file_name = deck_nickname.replace(" ", "-") + ".txt"
        print(file_name)
        f = open(deck_folder + "/" + file_name, "r")
        deck_files[deck_nickname] = f
    print(deck_files)

    for deck in decks:
        nickname = deck["Nickname"]
        print("nickname: ", nickname)
        deck_file = deck_files[nickname]
        print(deck_file)
        file_content = deck_file.read()
        print(file_content)
        file_lines = file_content.split("\n")

        cards = deck["ContainedObjects"]

        print("file_lines: {}, cards: {}".format(len(file_lines), len(cards)))
        assert len(cards) == len(file_lines)

        for i in range(len(cards)):
            cards[i]["Nickname"] = file_lines[i]
            card_nickname = cards[i]["Nickname"]
            if cards['Nickname'] == 'BS41-X07':
                continue
            nickname = card_nickname.replace("\t","")\
                            .replace("10thX-","10thX")\
                            .replace("X10TH","10thX")\
                            .replace("X10TH","10thX")\
                            .replace("RV-","RV ")
            try:
                cards['Description'] = card_effect[nickname]
            except:
                try:
                    cards['Description'] = card_effect[nickname.replace('-','')]
                except:
                    nickname=nickname.split('-')
                    cards['Description'] = card_effect[nickname[0]+"-"+nickname[1].zfill(3)]
        new_savefile_contents = json.dumps(save_object, indent=2)

    wf = open(userSavesPath + "TS_Save_-.json", "w")
    wf.write(new_savefile_contents)
    wf.close()
    print("Imported")