#!/usr/bin/python3

from mutagen.flac import FLAC

import os, sys, glob
from datetime import date

directory = "/home/fab/ogg/new"
if not os.path.isdir(directory):
  print("directory not found - only works on hel")
  sys.exit()

# curr_directory = os.getcwd()

os.chdir(directory)
result = glob.glob('**/*.flac', recursive=True)

print(result[0])
audio = FLAC(result[0])
for k in ['ARTIST', 'ALBUM', 'TITLE', 'DATE', 'GENRE', 'TRACKNUMBER', 'TRACKTOTAL', 'CDDB']:
  print(audio[k])

for a in range(len(result)):
  audio = FLAC(result[a])
  try:
    r = audio['DATE']
  except:
    print(a)
sys.exit()

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
      # print(i)
