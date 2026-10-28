#!/usr/bin/python3

from arena_sql import load_database_file, get_face_info

import sys

# --------------------------------------------------

database_file = sys.argv[1]

locstrings, cards, abilities, enums = load_database_file(database_file)

print(get_face_info(locstrings, abilities, cards[108029])["oracle_text"])
