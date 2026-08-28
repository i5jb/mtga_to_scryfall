#!/usr/bin/python3

from arena_constants import layouts, tag_desc
from arena_fix_strings import strip_string
from arena_sql import get_string, sql_locstrings, sql_cards

import sys
import json
import sqlite3

database_file = sys.argv[1]

with sqlite3.connect(database_file) as conn:
  conn.row_factory = sqlite3.Row

  locstrings = sql_locstrings(conn)
  cards = sql_cards(conn)

def get_name(card):
  name = get_string(locstrings, int(card["TitleId"]))
  # if card["AltTitleId"] != 0:
  #   flavor_name = get_string(locstrings, int(card["AltTitleId"]))
  #   name = f"{name} ({flavor_name})"
  # if card["InterchangeableTitleId"] != 0:
  #   printed_name = get_string(locstrings, int(card["InterchangeableTitleId"]))
  #   name = f"{name} ({printed_name})"
  return name

card_names = set()
for key in cards.keys():
  card = cards[key]

  if not card["IsPrimaryCard"]: continue
  if not card["IsDigitalOnly"]: continue

  layout = layouts[card["LinkedFaceType"]]
  links = [] if card["LinkedFaceGrpIds"] == '' \
             else card["LinkedFaceGrpIds"].split(",")
  match layout:
    case "Normal":
      normal = cards[key]
      card_names.add(get_name(normal))
    case "Transform Front":
      transform_front = cards[key]
      transform_back = cards[int(links[0])]
      card_names.add(f"{get_name(transform_front)} // {get_name(transform_back)}")
    case "Meld Piece":
      meld_piece = cards[key]
      meld_result = cards[int(links[0])]
      card_names.add(get_name(meld_piece))
      card_names.add(get_name(meld_result))
    case "Split Parent":
      split_parent = cards[key]
      split_face_1 = cards[int(links[0])]
      split_face_2 = cards[int(links[1])]
      card_names.add(get_name(split_parent))
    case "Adventurer":
      adventurer = cards[key]
      adventure = cards[int(links[0])]
      card_names.add(f"{get_name(adventurer)} // {get_name(adventure)}")
    case "Modal Front":
      modal_front = cards[key]
      modal_back = cards[int(links[0])]
      card_names.add(f"{get_name(modal_front)} // {get_name(modal_back)}")
    case "Specializer":
      specializer = cards[key]
      specialized_w = cards[int(links[0])]
      specialized_u = cards[int(links[1])]
      specialized_b = cards[int(links[2])]
      specialized_r = cards[int(links[3])]
      specialized_g = cards[int(links[4])]
      card_names.add(get_name(specializer))
      card_names.add(get_name(specialized_w))
      card_names.add(get_name(specialized_u))
      card_names.add(get_name(specialized_b))
      card_names.add(get_name(specialized_r))
      card_names.add(get_name(specialized_g))
    case "Prototype":
      prototype = cards[key]
      prototyped = cards[int(links[0])]
      card_names.add(get_name(prototype))
    case "Room Parent":
      room_parent = cards[key]
      room_left  = cards[int(links[0])]
      room_right = cards[int(links[1])]
      card_names.add(get_name(room_parent))
    case "Ominous":
      ominous = cards[key]
      omen = cards[int(links[0])]
      card_names.add(f"{get_name(ominous)} // {get_name(omen)}")
    case "Preparer":
      preparer = cards[key]
      prepared = cards[int(links[0])]
      card_names.add(f"{get_name(preparer)} // {get_name(prepared)}")
    case _:
      print(f"BAD LAYOUT {layout} -- Arena Id: {card["GrpId"]} ;; {card["ExpansionCode"]}:{card["CollectorNumber"]}")

known_bad_names = [
  # Not sure how a forest slipped into the Digital Only set
  "Forest",

  # Only Sparky / computer opponents use, and aren't craftable
  "Blinding Radiance",
  "Goblin Bruiser",
  "Ogre Painbringer",
  "Titanic Pelagosaur",
  "Treetop Recluse",
]

card_names = [name for name in card_names if name not in known_bad_names]
json.dump(sorted(list(card_names)), sys.stdout, indent=2, ensure_ascii=False)
