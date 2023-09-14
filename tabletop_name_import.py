import json
import os

userSavesPath = os.path.expanduser("~/Documents/My Games/Tabletop Simulator/Saves/")
with open(f"{os.path.dirname(os.path.realpath(__file__))}/effect_json/chinese.json", "r", encoding="utf-8") as f:
    ch_dict = json.load(f)
with open(f"{os.path.dirname(os.path.realpath(__file__))}/effect_json/english.json", "r", encoding="utf-8") as f:
    en_dict = json.load(f)


def get_description(nickname):
    nickname_save = nickname
    # Add chinese
    nickname = nickname.replace("\t", "") \
        .replace("10thX-", "10thX") \
        .replace("X10TH", "10thX") \
        .replace("X10TH", "10thX") \
        .replace("RV-", "RV ")
    try:
        description = ch_dict[nickname]
    except:
        try:
            description = ch_dict[nickname.replace("-", "")]
        except:
            try:
                nickname = nickname.split("-")
                description = ch_dict[nickname[0] + "-" + nickname[1].zfill(3)]
            except:
                print("Status error on card: " + nickname_save)
                description = "bad - let us know!"

    # Add english
    nickname = nickname_save
    if en_dict[nickname] == "-" or en_dict[nickname] == "":
        return
    try:
        description = description + "\n\n" + en_dict[nickname] + "\nTranslation from Fandom Wiki"
    except:
        try:
            description = description + "\n\n" + \
                          en_dict[nickname.replace("-", "")] + "\nTranslation from Fandom Wiki"
        except:
            try:
                nickname_save = nickname.split("-")
                description = description + "\n\n" + en_dict[nickname[0] + "-" +
                                nickname[1].zfill(3)] + "\nTranslation from Fandom Wiki"
            except:
                print("Effect error on card: " + nickname_save)
                description = description + "\n\nbad - let us know!"
    return description


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

    deck_files = {}
    for deck_nickname in decks_to_rename:
        file_name = deck_nickname.replace(" ", "-") + ".txt"
        f = open(deck_folder + "/" + file_name, "r")
        deck_files[deck_nickname] = f


    for deck in decks:
        nickname = deck["Nickname"]
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
            if cards['Nickname'] == 'BS41-X07':
                continue

            cards["Description"] = get_description(card_nickname)
        new_savefile_contents = json.dumps(save_object, indent=2)

    wf = open(userSavesPath + "TS_Save_-.json", "w")
    wf.write(new_savefile_contents)
    wf.close()
    print("Imported")
