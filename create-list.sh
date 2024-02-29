#!/usr/bin/python3

import os, sys, glob

flac_directory = "/home/fab/ogg/new"
if not os.path.isdir("flac_directory"):
  print("flac directory not found - only works on hel")
  sys.exit()

curr_directory = os.getcwd()

os.chdir(flac_directory)
result = glob.glob('**/*.flac', recursive=True)
#print(result)
os.chdir(curr_directory)
result.sort()

infile = open('cd-list-raw-length')
cd_list = infile.read()
infile.close()
# print(cd_list)

changes = False

outfile = open('cd-list-raw-length', 'a')
for r in result:
  song = r[0:-5]
  if song not in cd_list:
    print("adding " + song)
    changes = True
    # here we now call metaflac to get the length of the song
    l = os.popen('metaflac --show-total-samples "' + flac_directory + '/' + r + '"').read()
    outfile.write(song + ' / ' + l)

if changes:
  os.popen('sort cd-list-raw-length -o cd-list-raw-length')
