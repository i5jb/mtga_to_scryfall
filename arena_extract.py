#!/usr/bin/python3

from arena_constants import layouts
from arena_sql import get_full_card_name, load_database_file, to_arena_card

import sys
import json

# --------------------------------------------------

database_file = sys.argv[1]
list_of_digital_cards_file = sys.argv[2]
scryfall_file = sys.argv[3]

locstrings, cards, abilities, enums = load_database_file(database_file)

with open(list_of_digital_cards_file, "r") as f:
  list_of_digital_cards = json.loads(f.read())

with open(scryfall_file, "r") as f:
  scryfall = json.loads(f.read())

# --------------------------------------------------

cards_by_name = {}
for card in cards.values():
  if card["IsToken"]: continue
  if card["TitleId"] == 0: continue
  name = get_full_card_name(cards, locstrings, card)

  if name in cards_by_name: continue
  cards_by_name[name] = card

# --------------------------------------------------

arena_cards = {}
for name in list_of_digital_cards:
  if name not in cards_by_name:
    print(f"Not in Arena -- {name}", file=sys.stderr)
    continue
  if name not in scryfall:
    print(f"Not in Scryfall -- {name}", file=sys.stderr)
    continue
  card = cards_by_name[name]

  arena_card = to_arena_card(locstrings, cards, abilities, card)
  arena_cards[name] = arena_card

# for name in list_of_digital_cards:
#   arena_cards[name]["oracle_id"] = scryfall[name]["oracle_id"]

json.dump(arena_cards, sys.stdout, indent=2, ensure_ascii=False)

