import json
import glob
import time
import os
userSavesPath = os.path.expanduser("~/Documents/My Games/Tabletop Simulator/Saves/")
with open(f'{os.path.dirname(os.path.realpath(__file__))}/effect_json/chinese.json', 'r', encoding='utf-8') as f:
    card_effect = json.load(f)

    
with open(f'{userSavesPath}TS_Save_1.json', 'r', encoding='utf-8') as file:
    tt_dict = json.load(file)
    # print(tt_dict)

print(tt_dict["ObjectStates"])
for deck in tt_dict["ObjectStates"]:
    if deck['Name'] != "Infinite_Bag" or deck['Nickname'] == '':
            continue
    for card in deck['ContainedObjects'][0]['ContainedObjects']:
        nickname = card['Nickname']
        print(nickname)
        if (card['GUID'] == "" and card['Nickname'] == "") or card['Nickname'] == 'BS41-X07':
            continue
            
        nickname = nickname.replace("\t","")\
                           .replace("10thX-","10thX")\
                           .replace("X10TH","10thX")\
                           .replace("X10TH","10thX")\
                           .replace("RV-","RV ")
        try:
            card['Description'] = card_effect[nickname]
        except:
            try:
                card['Description'] = card_effect[nickname.replace('-','')]
            except:
                nickname=nickname.split('-')
                card['Description'] = card_effect[nickname[0]+"-"+nickname[1].zfill(3)]
                

with open('{userSavesPath}TS_Save_1.json', 'w', encoding='utf-8') as file:
    json.dump(tt_dict, file, ensure_ascii=False, indent=4)