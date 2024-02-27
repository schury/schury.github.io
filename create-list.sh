#!/usr/bin/python3

import os, platform
import glob

print(platform.node())

flac_directory = "/home/fab/ogg/new"
curr_directory = os.getcwd()
#files = []
#for f in os.listdir(directory):
  #files.append(f)

#files.sort()
#print(files)

os.chdir(flac_directory)
#result = glob.glob(directory + '/**/*.flac', recursive=True)
result = glob.glob('**/*.flac', recursive=True)
#print(result)
os.chdir(curr_directory)
result.sort()

#for f in files:
  #with open("songs/" + f) as file:
    #for l in file:
        #if "<h1>" in l:
          #print(l.removeprefix("<h1>").removesuffix("</h1>\n"))

infile = open('cd-list-raw-length')
cd_list = infile.read()
infile.close()
# print(cd_list)

outfile = open('cd-list-raw-length', 'a')
for r in result:
  song = r[0:-5]
  if song not in cd_list:
    print("adding " + song)
    # here we now call metaflac to get the length of the song
    t = 'metaflac --show-total-samples "' + flac_directory + '/' + r + '"'
    # print(t)
    l = os.popen('metaflac --show-total-samples "' + flac_directory + '/' + r + '"').read()
    # print(l)
    outfile.write(song + ' / ' + l)

os.popen('sort cd-list-raw-length > ttttemp')
os.popen('mv -f ttttemp cd-list-raw-length')
