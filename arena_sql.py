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
