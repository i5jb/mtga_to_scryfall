#!/usr/bin/python3

import json
import sys

main_dict_file = sys.argv[1]
list_of_keys_file = sys.argv[2]
with open(main_dict_file, "r") as f:
  main_dict = json.loads(f.read())
with open(list_of_keys_file, "r") as f:
  list_of_keys = json.loads(f.read())

subset = {}
for key in list_of_keys:
  if key not in main_dict:
    print(f"Bad key -- {key}", file=sys.stderr)
    continue
  subset[key] = main_dict[key]

json.dump(subset, sys.stdout, indent=2, ensure_ascii=False)
