#!/usr/bin/python3

layouts = [
  "Normal",          # No links                   -- PRIMARY
  "Transform Back",  # Links to 1 Transform From
  "Transform Front", # Links to 1 Transform Back  -- PRIMARY
  "Meld Result",     # Links to 2 Meld Pieces
  "Meld Piece",      # Links to 1 Meld Result     -- PRIMARY
  "Split Face",      # Links to 1 Split Parent
  "Split Parent",    # Links to 2 Split Face      -- PRIMARY
  "Adventure",       # Links to 1 Adventurer
  "Adventurer",      # Links to 1 Adventure       -- PRIMARY
  "Modal Back",      # Links to 1 Modal Front
  "Modal Front",     # Links to 1 Modal Back      -- PRIMARY
  "Specialized",     # Links to 1 Specializer
  "Specializer",     # Links to 5 Specialized     -- PRIMARY
  "Prototyped",      # Links to 1 Prototype
  "Prototype",       # Links to 1 Prototyped      -- PRIMARY
  "Room",            # Links to 1 Room Parent
  "Room Parent",     # Links to 2 Rooms           -- PRIMARY
  "Omen",            # Links to 1 Ominous
  "Ominous",         # Links to 1 Omen            -- PRIMARY
  "Preparer",        # Links to 1 Prepared        -- PRIMARY
  "Prepared",        # Links to 1 Preparer
]

tag_desc = {
    "380044820": "Joinable Keywords",

  "-1652955139": "Behold a Merfolk",
    "562854450": "Behold a Goblin",
   "1536710623": "Behold a Kithkin",
  "-1017350410": "Behold an Elemental",
   "1560405038": "Behold an Elf",
  "-1908305635": "Behold a Hero",
    "-32672675": "Behold a Gamma",
   "1939436126": "Behold a Dragon",

   "-233436354": "Behold and Exile",

    "561908357": "Behold of choice",

  "-1882160459": "Evoke Mana",

  "-2098885201": "Anchor Words",
    "511010486": "Paw Modes",

   "1411227424": "When the Nth plan counter is put on ...",

    "486419830": "Protection",
   "-643095595": "Control Player",
    "520549389": "Land Mayhem",
   "1225149333": "Waterbend {X}",
}
