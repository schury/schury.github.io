#!/usr/bin/python3

import os, platform

print(platform.node())

directory = "songs"
files = []
for f in os.listdir(directory):
  files.append(f)

files.sort()

for f in files:
  with open("songs/" + f) as file:
    for l in file:
        if "<h1>" in l:
          print(l.removeprefix("<h1>").removesuffix("</h1>\n"))

infile = open("cd-list-raw-length")
cd_list = infile.read()

if "Zandelle" in cd_list:
  print("yes")
