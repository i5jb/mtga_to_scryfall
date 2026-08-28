#!/usr/bin/python3

import json
import sys

from download_tools import (
  save_to_file,
  download_file_and_save_to_cache,
  download_file_or_read_from_cache,
  download_and_gunzip_file_or_read_from_cache
)

# ----------------------------------------------------------

debug = False

# ----------------------------------------------------------

url   = "https://api.scryfall.com/bulk-data/oracle-cards"
cache = "cache/scryfall-bulk-data-oracle-cards"

scryfall_bulk_file = download_file_and_save_to_cache(url, cache)
#scryfall_bulk_file = download_file_or_read_from_cache(url, cache)
scryfall_bulk_json = json.loads(scryfall_bulk_file.decode("utf-8"))

if debug:
  json.dump(scryfall_bulk_json, sys.stdout, indent=2, ensure_ascii=False)
  print()

### In that file (json file):
# {
#   "object": "bulk_data",
#   "id": "27bf3214-1271-490b-bdfe-c0be6c23d02e",
#   "type": "oracle_cards",
#   "updated_at": "2026-08-28T21:01:53.804+00:00",
#   "uri": "https://api.scryfall.com/bulk-data/27bf3214-1271-490b-bdfe-c0be6c23d02e",
#   "name": "Oracle Cards",
#   "description": "A JSON file containing one Scryfall card object for each Oracle ID on Scryfall. The chosen sets for the cards are an attempt to return the most up-to-date recognizable version of the card.",
#   "jsonl_download_uri": "https://data.scryfall.io/oracle-cards/oracle-cards-20260828210153.jsonl.gz",
#   "compressed_size": 24532450
# }
# : https://assets.mtgarena.wizards.com/External_14056_1313448.mtga

assert("jsonl_download_uri" in scryfall_bulk_json)

jsonl_download_uri = scryfall_bulk_json["jsonl_download_uri"]
oracle_jsonl_filename = jsonl_download_uri.split("/")[-1].strip(".gz")
url   = f"{jsonl_download_uri}"
cache = f"cache/{oracle_jsonl_filename}"

oracle_jsonl_file = download_and_gunzip_file_or_read_from_cache(url, cache)

# In that file (jsonl file):
#  The database we care about

save_to_file(oracle_jsonl_file, "oracle-cards.jsonl")
