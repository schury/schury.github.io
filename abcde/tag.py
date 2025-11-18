#!/usr/bin/python3

import mutagen
from mutagen.easyid3 import EasyID3

import os, sys, glob
from datetime import date

mp3_directory = "/home/fab/ogg/mp3s"
if not os.path.isdir(mp3_directory):
  print("directory not found - only works on hel")
  sys.exit()

curr_directory = os.getcwd()

os.chdir(mp3_directory)
result = glob.glob('**/*.mp3', recursive=True)

# print(EasyID3.valid_keys.keys())
# tag['date'] = '2025'
# tag.save(v2_version=3)

for i in ['Heaven Shall Burn - [2025] Heimat.mp3']:
  tag = EasyID3(i)
  # for k in ['date']:
  for k in EasyID3.valid_keys.keys():
    try:
      r = tag[k]
      print(k, r)
    except: 
      True
      #print(i)
