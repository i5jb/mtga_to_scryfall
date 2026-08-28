import os
import requests
import gzip

# ----------------------------------------------------------

def download_file(url):
  response_raw = requests.get(url, headers = { 'user-agent': 'mtga_to_scryfall/1.0'})
  if (response_raw.status_code != 200):
    raise Exception(f"{response_raw.status_code}: {url}")
  return response_raw.content

def save_to_file(data, cache):
  with open(cache, "wb") as f:
    f.write(data)

def read_from_file(cache):
  with open(cache, "rb") as f:
    return f.read()

def file_exists(cache):
  return os.path.exists(cache)

# ----------------------------------------------------------

def download_file_and_save_to_cache(url, cache):
  print(f"Download: {url}")
  data = download_file(url)
  save_to_file(data, cache)
  return data

def download_file_or_read_from_cache(url, cache):
  if file_exists(cache):
    print(f"Using cache'd file: {cache}")
    data = read_from_file(cache)
  else:
    print(f"Download: {url}")
    data = download_file(url)
    save_to_file(data, cache)
  return data

def download_and_gunzip_file_or_read_from_cache(url, cache):
  if file_exists(cache):
    print(f"Using cache'd file: {cache}")
    data = read_from_file(cache)
  else:
    print(f"Download: {url}")
    compressed = download_file(url)
    data = gzip.decompress(compressed)
    save_to_file(data, cache)
  return data
