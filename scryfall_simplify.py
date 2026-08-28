#!/usr/bin/python3

import json
import sys

from download_tools import read_from_file

scryfall_file = sys.argv[1]
oracle_lines = read_from_file(scryfall_file).decode("utf-8").strip().split("\n")
oracle_cards = []
for line in oracle_lines:
  oracle_cards.append(json.loads(line))

variant_cards = {
  "Everythingamajig",
  "Garbage Elemental",
  "Ineffable Blessing",
  "Knight of the Kitchen Sink",
  "Scavenger Hunt",
  "Sly Spy",
  "The Superlatorium",
  "Trivia Contest",
  "Very Cryptic Command",
}

simplified_cards = {}
for card in oracle_cards:
  if card["layout"] == "token": continue
  if card["layout"] == "double_faced_token": continue
  if card["layout"] == "front_card": continue
  if card["name"] in variant_cards: continue

  if (card["name"] == "B.F.M. (Big Furry Monster)"): continue

  if (card["name"] == "Artist Alley") and (card["set"] == "unk"): continue
  if (card["name"] == "Artist Alley") and (card["set"] == "punk"): continue

  if (card["name"] == "Fast // Furious") and (card["set"] == "unk"): continue
  if (card["name"] == "Joven and Chandler") and (card["set"] == "unk"): continue
  if (card["name"] == "No Way Out") and (card["set"] == "punk"): continue
  if (card["name"] == "Pick Your Poison") and (card["set"] == "cmb2"): continue
  if (card["name"] == "Red Herring") and (card["set"] == "cmb2"): continue
  if (card["name"] == "Unquenchable Fury") and (card["set"] == "tbth"): continue

  oracle_id = card["oracle_id"]
  layout = card["layout"]
  name = card["name"]
  type_line = card["type_line"]

  simplified_card = {}
  simplified_card["oracle_id"] = card["oracle_id"]
  simplified_card["name"] = card["name"]
  simplified_card["layout"] = card["layout"]
  simplified_card["type_line"] = card["type_line"]

  if "mana_cost" in card and \
     card["mana_cost"] != "": simplified_card["mana_cost"] = card["mana_cost"]
  if "color_indicator" in card: simplified_card["color_indicator"] = card["color_indicator"]
  if "oracle_text" in card: simplified_card["oracle_text"] = card["oracle_text"]
  if "power" in card: simplified_card["power"] = card["power"]
  if "toughness" in card: simplified_card["toughness"] = card["toughness"]
  if "loyalty" in card: simplified_card["loyalty"] = card["loyalty"]
  if "life_modifier" in card: simplified_card["life_modifier"] = card["life_modifier"]
  if "hand_modifier" in card: simplified_card["hand_modifier"] = card["hand_modifier"]

  if "card_faces" in card:
    simplified_card["card_faces"] = []
    for face in card["card_faces"]:
      card_face = {}
      if "name" in face: card_face["name"] = face["name"]
      if "type_line" in face: card_face["type_line"] = face["type_line"]
      if "mana_cost" in face and \
         face["mana_cost"] != "": card_face["mana_cost"] = face["mana_cost"]
      if "color_indicator" in face: card_face["color_indicator"] = face["color_indicator"]
      if "oracle_text" in face: card_face["oracle_text"] = face["oracle_text"]
      if "power" in face: card_face["power"] = face["power"]
      if "toughness" in face: card_face["toughness"] = face["toughness"]
      if "defense" in face: card_face["defense"] = face["defense"]
      if "loyalty" in face: card_face["loyalty"] = face["loyalty"]
      simplified_card["card_faces"].append(card_face)

  if name in simplified_cards:
    print(f"Duplicate name? -- {name}")
  simplified_cards[name] = simplified_card

sorted_by_name = {}
for name in sorted(simplified_cards.keys()):
  sorted_by_name[name] = simplified_cards[name]
json.dump(sorted_by_name, sys.stdout, indent=2, ensure_ascii=False)
