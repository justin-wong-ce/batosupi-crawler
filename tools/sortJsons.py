import json
import os
from collections import OrderedDict

with open(f'{os.path.dirname(os.path.realpath(__file__))}/effect_json/chinese.json', 'r',
          encoding='utf-8') as f:
    card_list = OrderedDict(json.load(f))
with open(f'{os.path.dirname(os.path.realpath(__file__))}/effect_json/chinese.json', 'w', encoding='utf-8') as f:
    json.dump(card_list, f, ensure_ascii=False, sort_keys=True)

with open(f"{os.path.dirname(os.path.realpath(__file__))}/effect_json/english.json",
          "r", encoding="utf-8") as f:
    card_list = OrderedDict(json.load(f))
with open(f"{os.path.dirname(os.path.realpath(__file__))}/effect_json/english.json", "w", encoding="utf-8") as f:
    json.dump(card_list, f, ensure_ascii=False, sort_keys=True)
