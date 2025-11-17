#!/usr/bin/python3

import mutagen
from mutagen.easyid3 import EasyID3

# print(EasyID3.valid_keys.keys())
# tag['date'] = '2025'
# tag.save(v2_version=3)

tag = EasyID3('test.mp3')
for k in EasyID3.valid_keys.keys():
  try:
    r = tag[k]
    print(k, r)
  except: 
    True
