#!/usr/bin/python3

from arena_sql import load_database_file, get_full_card_name, to_arena_card

import sys
import json

# --------------------------------------------------

def has_spellbook_words(s):
  return ("spellbook" in s) or \
         ("Spellbook" in s) or \
         ("Power Nine" in s)

# --------------------------------------------------

database_file = sys.argv[1]

locstrings, cards, abilities, enums = load_database_file(database_file)

cards_by_name = {}
for card in cards.values():
  if card["IsToken"]: continue
  if card["TitleId"] == 0: continue
  name = get_full_card_name(cards, locstrings, card)

  if name in cards_by_name: continue
  cards_by_name[name] = card

for name in sorted(cards_by_name.keys()):
  card = cards_by_name[name]
  arena_card = to_arena_card(locstrings, cards, abilities, card)
  if arena_card == None: continue

  # Any card that conjures something (not just spellbooks), has conjurations
  # We only want to return cards that say "spellbook" (or something like it)
  has_spellbook = False
  if arena_card["layout"] == "normal":
    has_spellbook = has_spellbook_words(arena_card["oracle_text"])
  if arena_card["layout"] == "adventure":
    has_spellbook = has_spellbook_words(arena_card["card_faces"][0]["oracle_text"]) or \
                    has_spellbook_words(arena_card["card_faces"][1]["oracle_text"])
  if not has_spellbook: continue

  # The spellbook of some cards is on the adventure and doesn't show up
  # on the front side 'AbilityIdToLinkedConjurations' field. So check
  # all sides.
  links = [] if card["LinkedFaceGrpIds"] == '' \
             else card["LinkedFaceGrpIds"].split(",")
  links = [card] + [cards[int(link)] for link in links]

  for link in links:
    conjurations = link['AbilityIdToLinkedConjurations']
    if conjurations != "":
      entries = conjurations.split(",")
      if len(entries) == 1: continue

      spellbook = []
      for entry in entries:
        ability, ref_type, name_ref = entry.split(":")
        spellbook.append(get_full_card_name(cards, locstrings, cards[int(name_ref)]))
      if len(spellbook) > 0:
        json.dump({ 'name': name, 'spellbook': spellbook}, sys.stdout, ensure_ascii=False)
        print()

