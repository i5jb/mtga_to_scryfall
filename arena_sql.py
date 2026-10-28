#!/usr/bin/python3

from arena_fix_strings import strip_string

def get_string(locstrings, id):
  def get(id):
    if (id, 1) in locstrings: return locstrings[(id,1)] # (id,1) = HTML style formatting
    #if (id, 0) in locstrings: return locstrings[(id,0)] # (id,0) = Raw formatting
    #if (id, 2) in locstrings: return locstrings[(id,2)] # (id,2) = Ascii-only formatting
    raise("Unknown locstring")
  return strip_string(get(id))

def sql_locstrings(conn):
  locstrings = {}

  cursor = conn.cursor()
  cursor.execute("SELECT * FROM Localizations_enUS")
  dbstrings = cursor.fetchall()
  for dbstring in dbstrings:
    (LocId, Formatted, Loc) = dbstring['LocId'], dbstring['Formatted'], dbstring['Loc']
    locstrings[(LocId, Formatted)] = Loc

  return locstrings

def sql_cards(conn):
  cards = {}

  cursor = conn.cursor()
  cursor.execute("SELECT * FROM Cards")
  dbcards = cursor.fetchall()
  for dbcard in dbcards:
    if (dbcard['TitleId'] == 0): continue
    cards[dbcard['GrpId']] = dict(dbcard)

  return cards

def sql_enums(conn, locstrings):
  enums = {}

  cursor = conn.cursor()
  cursor.execute("SELECT * FROM Enums")
  dbenums = cursor.fetchall()
  for dbenum in dbenums:
    if dbenum["Type"] not in enums:
      enums[dbenum["Type"]] = {}
    enums[dbenum["Type"]][dbenum["Value"]] = get_string(locstrings, dbenum["LocId"])

  return enums

def sql_abilities(conn):
  abilities = {}

  cursor = conn.cursor()
  cursor.execute("SELECT * FROM Abilities")
  dbabilities = cursor.fetchall()
  for dbability in dbabilities:
    abilities[dbability["Id"]] = dict(dbability)

  return abilities

# ----------------------------------------

import sqlite3

def load_database_file(database_file):
  with sqlite3.connect(database_file) as conn:
    conn.row_factory = sqlite3.Row

    locstrings = sql_locstrings(conn)
    cards = sql_cards(conn)
    abilities = sql_abilities(conn)
    enums = sql_enums(conn, locstrings)

  return locstrings, cards, abilities, enums

# --------------------------------------------------

# Tags are part of the ability info table.
#
# Ex:
#  {
#    "Id": 8,      # Flying
#    "BaseId": 0,
#    "TextId": 46, # "Flying"
#    ...
#    "Tags": "-127354192,380044820,-839465756,322893110",
#    ...
#  }
#
# Where "Tags" is either a comman separated list, or None.
#
# In some cases, like the speicific Wards (Ward {1}, Ward {2},
#  Ward-Pay 2 life, etc), there are no tags. Instead, "BaseId"
#  is a pointer to a generic parent ability. The parent ability
#  has the tags.
#
# Ex:
#  {
#    "Id": 1577,   # Ward-Pay 2 life
#    "BaseId": 211,  # The link to generic "Ward"
#    "TextId": 605033,, # "Ward-Pay 2 life"
#    ...
#    "Tags": None,
#    ...
#  }
#  {
#    "Id": 211,      # Generic Ward
#    "BaseId": 0,
#    "TextId": 495960, # "Ward"
#    ...
#    "Tags": "-127354192,380044820,-839465756",
#    ...
#  }
#
# The only tag we care about is 380044820 ("Joinable Keywords").

from arena_constants import tag_desc

def get_tags(abilities, ability_info):
  # Base case, get tags directly from this ability line
  if ability_info["Tags"] != None:
    return ability_info["Tags"]

  # Inheritance case, get tags from parent ability
  if ability_info["BaseId"] != 0:
    if abilities[ability_info["BaseId"]]["Tags"] != None:
      return abilities[ability_info["BaseId"]]["Tags"]

  # No tags found
  return None

# Convert tag IDs to strings

def get_tag_strings(abilities, ability_info):
  tags = get_tags(abilities, ability_info)
  if tags == None: return []
  return [tag_desc.get(tag_id, "UNKNOWN") for tag_id in tags.split(",")]

# --------------------------------------------------

from arena_constants import layouts

def get_name(locstrings, card):
  return get_string(locstrings, int(card["TitleId"]))

def get_full_card_name(cards, locstrings, card):
  layout = layouts[card["LinkedFaceType"]]
  links = [] if card["LinkedFaceGrpIds"] == '' \
             else card["LinkedFaceGrpIds"].split(",")
  match layout:
    case "Transform Front":
      transform_front = card
      transform_back = cards[int(links[0])]
      return f"{get_name(locstrings, transform_front)} // {get_name(locstrings, transform_back)}"
    case "Modal Front":
      modal_front = card
      modal_back = cards[int(links[0])]
      return f"{get_name(locstrings, modal_front)} // {get_name(locstrings, modal_back)}"
    case "Adventurer":
      adventurer = card
      adventure = cards[int(links[0])]
      return f"{get_name(locstrings, adventurer)} // {get_name(locstrings, adventure)}"
    case "Ominous":
      ominous = card
      omen = cards[int(links[0])]
      return f"{get_name(locstrings, ominous)} // {get_name(locstrings, omen)}"
    case "Preparer":
      preparer = card
      prepared = cards[int(links[0])]
      return f"{get_name(locstrings, preparer)} // {get_name(locstrings, prepared)}"

  return get_name(locstrings, card)

# --------------------------------------------------

def get_color_indicator(indicator):
  result = []
  colors = ["W", "U", "B", "R", "G"]
  for color_index in indicator.split(","):
    result.append(colors[int(color_index) - 1])
  return sorted(result)

import re
from arena_fix_strings import fix_mana_cost

def get_chapter_prefix(chapter_number):
  return ["I", "II", "III", "IV", "V", "VI"][chapter_number - 1]

SAGA_CHAPTER_ID = 166
station_re = re.compile(r"STATIONLEVEL \[(\d*\+)] \[((\d*)\/(\d*))?] \[.*]")
def get_oracle_text(locstrings, abilities, ability_ids):
  result = ""

  has_chapters = False
  last_chapter = "I"
  chapter_prefix = ""
  chapter_text = ""

  first_line = True
  last_line_was_joinable_keyword = False
  last_line_was_station = False
  for ability in ability_ids.split(","):
    [ability_id, ability_loc_id] = ability.split(":")
    ability_info = abilities[int(ability_id)]
    #json.dump(ability_info, sys.stdout, indent=2, ensure_ascii=False)

    # Saga abilities / Chapters are a little messy
    #
    # In the datafile, each chapter is a different ability line,
    #  but on the card, we want to group them.
    # For example, in the datafile you might have:
    #  I. Draw a card.
    #  II. Draw a card.
    #  III. Draw two cards
    # We want:
    #  I, II. Draw a card.
    #  III. Draw two cards.
    # We also need to track which chapter is the final chapter
    #  for the reminder text, which says "(... sacrifice after III.)"
    #
    if ability_info["BaseId"] == SAGA_CHAPTER_ID:
      has_chapters = True
      chapter_number = ability_info["BaseIdNumeral"]
      line = get_string(locstrings, int(ability_loc_id)).replace(" \n", "\n")

      last_chapter = get_chapter_prefix(chapter_number)
      if chapter_number == 1:
        chapter_prefix = get_chapter_prefix(chapter_number)
        chapter_text = line
      elif chapter_number > 1 and line != chapter_text:
        result += f"{chapter_prefix} — {chapter_text}\n"

        chapter_prefix = get_chapter_prefix(chapter_number)
        chapter_text = line
      elif chapter_number > 1 and line == chapter_text:
        chapter_prefix = f"{chapter_prefix}, {get_chapter_prefix(chapter_number)}"
      continue

    ability_tags = get_tag_strings(abilities, ability_info)
    is_joinable_keyword = "Joinable Keywords" in ability_tags

    loyalty_cost = ability_info["LoyaltyCost"]
    if loyalty_cost != None: loyalty_cost = loyalty_cost.replace("-", "−")

    line = get_string(locstrings, int(ability_loc_id)).replace(" \n", "\n")

    # The CLASSLEVEL line doesn't tell us antyhing elseful, and
    #  we want to skip over it entirely. This needs to be done before
    #  accidentally putting in a newline.
    if line.startswith("CLASSLEVEL"): continue

    if (not first_line) and (not last_line_was_station):
      if not last_line_was_joinable_keyword and is_joinable_keyword:
        result += "\n"
      if not is_joinable_keyword:
        result += "\n"

    # The STATIONLEVEL line does have useful information:
    #  STATIONLEVEL [6+] [2/3] [Flying] [Deathtouch] [Lifelink]
    # Mainly, the station requirement (the "6+" above)
    if line.startswith("STATIONLEVEL"):
      match = station_re.match(line)
      station_number, power_toughness, power, toughness = match.groups()
      result += f"{station_number} | "
      last_line_was_station = True
      continue
    else:
      last_line_was_station = False

    if       (is_joinable_keyword) and     (last_line_was_joinable_keyword): result += f", {line}"
    elif     (is_joinable_keyword) and (not last_line_was_joinable_keyword): result += f"{line}"
    elif (not is_joinable_keyword) and (loyalty_cost == None):               result += f"{line}"
    elif (not is_joinable_keyword) and (loyalty_cost != None):               result += f"{loyalty_cost}: {line}"

    last_line_was_joinable_keyword = is_joinable_keyword
    first_line = False

  if has_chapters:
    result += f"{chapter_prefix} — {chapter_text}"
    result = \
      f"(As this Saga enters and after your draw step, add a " + \
      f"lore counter. Sacrifice after {last_chapter}.)\n" + \
      f"{result}"

  return result

def get_face_info(locstrings, abilities, card):
  # json.dump(card, sys.stdout, indent=2, ensure_ascii=False)

  cardtype = get_string(locstrings, card["TypeTextId"])
  subtype = ""
  if card["SubtypeTextId"] != 0:
    subtype = get_string(locstrings, card["SubtypeTextId"])
  if subtype != "": type_line = f"{cardtype} — {subtype}"
  else:             type_line = f"{cardtype}"

  face = {}
  face["name"] = get_name(locstrings, card)
  face["type_line"] = type_line
  if (card["OldSchoolManaText"] != ''):
    face["mana_cost"] = f"{fix_mana_cost(card["OldSchoolManaText"])}"
  if card["IndicatorColors"] != '':
    face["color_indicator"] = get_color_indicator(card["IndicatorColors"])
  if card["AbilityIds"] != '':
    face["oracle_text"] = get_oracle_text(locstrings, abilities, card["AbilityIds"])
  else:
    face["oracle_text"] = ""
  if (card["Power"] != '') and (card["Toughness"] != ''):
    face["power"] = card["Power"]
    face["toughness"] = card["Toughness"]
  #if "defense" in card: face["defense"] = card["defense"]
  if ("Planeswalker" in type_line):
    face["loyalty"] = card["Toughness"]

  return face

# --------------------------------------------------

def to_arena_card(locstrings, cards, abilities, card):
  arena_card = {}

  layout = layouts[card["LinkedFaceType"]]
  links = [] if card["LinkedFaceGrpIds"] == '' \
             else card["LinkedFaceGrpIds"].split(",")

  match layout:
    case "Normal" | "Specializer" | "Specialized":
      normal = card
      normal_face = get_face_info(locstrings, abilities, normal)

      arena_card["name"] = normal_face["name"]

      arena_card["layout"] = "normal"
      if "Saga"  in normal_face["type_line"]: arena_card["layout"] = "saga"
      if "Case"  in normal_face["type_line"]: arena_card["layout"] = "case"
      if "Class" in normal_face["type_line"]: arena_card["layout"] = "class"

      arena_card["type_line"] = normal_face["type_line"]

      if "mana_cost"   in normal_face: arena_card["mana_cost"]   = normal_face["mana_cost"]
      if "oracle_text" in normal_face: arena_card["oracle_text"] = normal_face["oracle_text"]
      if arena_card["layout"] == "class":
        arena_card["oracle_text"] = f"(Gain the next level as a sorcery to add its ability.)\n{arena_card["oracle_text"]}"
      if "power" in normal_face: arena_card["power"] = normal_face["power"]
      if "toughness" in normal_face: arena_card["toughness"] = normal_face["toughness"]
      if "loyalty" in normal_face: arena_card["loyalty"] = normal_face["loyalty"]

      return arena_card
    case "Transform Front":
      transform_front = card
      transform_back = cards[int(links[0])]

      transform_front_face = get_face_info(locstrings, abilities, transform_front)
      transform_back_face  = get_face_info(locstrings, abilities, transform_back)

      arena_card["name"] = f"{transform_front_face["name"]} // {transform_back_face["name"]}"
      arena_card["layout"] = "transform"
      arena_card["type_line"] = f"{transform_front_face["type_line"]} // {transform_back_face["type_line"]}"

      arena_card["card_faces"] = [ transform_front_face, transform_back_face ]

      return arena_card

    case "Modal Front":
      modal_front = card
      modal_back = cards[int(links[0])]

      modal_front_face = get_face_info(locstrings, abilities, modal_front)
      modal_back_face  = get_face_info(locstrings, abilities, modal_back)

      arena_card["name"] = f"{modal_front_face["name"]} // {modal_back_face["name"]}"
      arena_card["layout"] = "modal_dfc"
      arena_card["type_line"] = f"{modal_front_face["type_line"]} // {modal_back_face["type_line"]}"

      arena_card["card_faces"] = [ modal_front_face, modal_back_face ]

      return arena_card

    case "Adventurer" | "Ominous":
      adventurer = card
      adventure = cards[int(links[0])]

      adventurer_face = get_face_info(locstrings, abilities, adventurer)
      adventure_face  = get_face_info(locstrings, abilities, adventure)

      arena_card["name"] = f"{adventurer_face["name"]} // {adventure_face["name"]}"
      arena_card["layout"] = "adventure"
      arena_card["type_line"] = f"{adventurer_face["type_line"]} // {adventure_face["type_line"]}"
      if "mana_cost" in adventurer_face: arena_card["mana_cost"] = f"{adventurer_face["mana_cost"]} // {adventure_face["mana_cost"]}"
      if "power" in adventurer_face: arena_card["power"] = f"{adventurer_face["power"]}"
      if "toughness" in adventurer_face: arena_card["toughness"] = f"{adventurer_face["toughness"]}"

      arena_card["card_faces"] = [ adventurer_face, adventure_face ]

      return arena_card

    case "Preparer":
      preparer = card
      prepared = cards[int(links[0])]

      preparer_face = get_face_info(locstrings, abilities, preparer)
      prepared_face  = get_face_info(locstrings, abilities, prepared)

      arena_card["name"] = f"{preparer_face["name"]} // {prepared_face["name"]}"
      arena_card["layout"] = "prepare"
      arena_card["type_line"] = f"{preparer_face["type_line"]} // {prepared_face["type_line"]}"
      arena_card["mana_cost"] = f"{preparer_face["mana_cost"]} // {prepared_face["mana_cost"]}"
      if "power" in preparer_face: arena_card["power"] = f"{preparer_face["power"]}"
      if "toughness" in preparer_face: arena_card["toughness"] = f"{preparer_face["toughness"]}"
      arena_card["card_faces"] = [ preparer_face, prepared_face ]

      return arena_card

    case "Split Parent":
      split_1 = cards[int(links[0])]
      split_2 = cards[int(links[1])]

      split_face_1 = get_face_info(locstrings, abilities, split_1)
      split_face_2 = get_face_info(locstrings, abilities, split_2)

      arena_card["name"] = f"{split_face_1["name"]} // {split_face_2["name"]}"
      arena_card["layout"] = "split"
      arena_card["type_line"] = f"{split_face_1["type_line"]} // {split_face_2["type_line"]}"
      arena_card["mana_cost"] = f"{split_face_1["mana_cost"]} // {split_face_2["mana_cost"]}"
      arena_card["card_faces"] = [ split_face_1, split_face_2 ]

      return arena_card

    case "Room Parent":
      room_left = cards[int(links[0])]
      room_right = cards[int(links[1])]

      room_left_face = get_face_info(locstrings, abilities, room_left)
      room_right_face = get_face_info(locstrings, abilities, room_right)

      arena_card["name"] = f"{room_left_face["name"]} // {room_right_face["name"]}"
      arena_card["layout"] = "split"
      arena_card["type_line"] = f"{room_left_face["type_line"]} // {room_right_face["type_line"]}"
      arena_card["mana_cost"] = f"{room_left_face["mana_cost"]} // {room_right_face["mana_cost"]}"
      arena_card["card_faces"] = [ room_left_face, room_right_face ]

      return arena_card

    case "Prototype":
      prototype = card
      prototyped = cards[int(links[0])]

      prototype_face = get_face_info(locstrings, abilities, prototype)
      prototyped_face = get_face_info(locstrings, abilities, prototyped)

      arena_card["name"] = f"{prototype_face["name"]}"
      arena_card["layout"] = "prototype"
      arena_card["type_line"] = f"{prototype_face["type_line"]}"
      arena_card["mana_cost"] = f"{prototype_face["mana_cost"]}"

      oracle_text = prototype_face["oracle_text"]
      oracle_text = oracle_text.replace("Prototype\n", f"Prototype {prototyped_face["mana_cost"]} — {prototyped_face["power"]}/{prototyped_face["toughness"]}\n")
      arena_card["oracle_text"] = oracle_text

      arena_card["power"] = f"{prototype_face["power"]}"
      arena_card["toughness"] = f"{prototype_face["toughness"]}"

      return arena_card

# --------------------------------------------------

