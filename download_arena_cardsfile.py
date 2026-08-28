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

url   = "https://mtgarena.downloads.wizards.com/Live/Windows64/version"
cache = "cache/version"

version_file = download_file_and_save_to_cache(url, cache)
#version_file = download_file_or_read_from_cache(url, cache)
version_json = json.loads(version_file.decode("utf-8"))

if debug:
  json.dump(version_json, sys.stdout, indent=2, ensure_ascii=False)
  print()

### In that file (json file):
# {
#     "VersionURL":  "https://mtgarena.downloads.wizards.com/Live/Windows64/version",
#     "Versions":  {
#                      "0.1.14056.1313448":  "8/19/26"
#                  },
#     "CurrentPatchURL":  "",
#     "Flavor":  "Live",
#     "ProductCode":  "{BB91E8E1-8030-43C7-8461-1E54166F3AAB}",
#     "CurrentInstallerURL":  "https://mtgarena.downloads.wizards.com/Live/Windows64/versions/14056.1313448/MTGAInstaller_0.1.14056.1313448.msi",
#     "Name":  "MTG Arena",
#     "BinaryURL":  "https://mtgarena.downloads.wizards.com/Live/Windows64/versions/",
#     "FileCount":  "468"
# }
### Extract Version
# 0.1.14056.1313448 8/19/26
# Version: 14056_1313448
# Manifest external URL: https://assets.mtgarena.wizards.com/External_14056_1313448.mtga

assert(len(version_json["Versions"].keys()) == 1)
version = list(version_json["Versions"].keys())[0]
version_str = "_".join(version.split(".")[-2:])

if debug:
  print(f"Version: {version}")
  print(f"Version String: {version_str}")

external_filename = f"External_{version_str}.mtga"
url   = f"https://assets.mtgarena.wizards.com/{external_filename}"
cache = f"cache/{external_filename}"

external_file = download_file_or_read_from_cache(url, cache)
external_text = external_file.decode("utf-8")

if debug:
  print(f"External Text: {external_text}")

### In that file (single line)
# e45a2530c0be4f84b9b998b0b9d255e6

manifest_filename = f"Manifest_{external_text}.mtga"
url   = f"https://assets.mtgarena.wizards.com/{manifest_filename}"
cache = f"cache/{manifest_filename}"

manifest_file = download_and_gunzip_file_or_read_from_cache(url, cache)
manifest_json = json.loads(manifest_file.decode("utf-8"))

if debug:
  json.dump(version_json, sys.stdout, indent=2, ensure_ascii=False)
  print()

### In that file (json file)
# {
#   "Assets": [
#     ...
#     {
#      "Name": "Raw_CardDatabase_6b61e838c6da4574edd31892f66d0f53.mtga",
#      "AssetType": "Raw",
#      "Length": 254304256,
#      "CompressedLength": 69747863,
#      "wrapper": "gz",
#      "Priority": 25,
#      "sha256": "BmZe+6iNbYIJa2JbYTTQCouvKxmomeEkPl9cHRLa75w=",
#      "IndexedAssets": []
#     },
#     ...
#   ]
# }
#
### Note: "Name" and "wrapper" fields.

card_databae_filename = None
for row in manifest_json["Assets"]:
  if row["Name"].startswith("Raw_CardDatabase_"):
    card_databae_filename = row["Name"]
    break

assert(card_databae_filename != None)

url   = f"https://assets.mtgarena.wizards.com/{card_databae_filename}.gz"
cache = f"cache/{card_databae_filename}"

manifest_file = download_and_gunzip_file_or_read_from_cache(url, cache)
save_to_file(manifest_file, "card_database.sqlite3")

# In that file (sqlite3 file):
#  The database we care about
