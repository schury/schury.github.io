#!/usr/bin/python3

import os, sys
from datetime import date




main_header = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rezepte</title>
  <link rel="stylesheet" href=\"css/rezepte.css\">
</head>
<body>
'''

rez_header = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TITLE</title>
  <link rel="stylesheet" href=\"../css/rezepte.css\">
</head>
<body>
'''

title = ''
zutaten = []
zubereitung = []

infiles = ['rezepte/hauptgerichte.txt', 'rezepte/nachspeisen.txt']

mode = 'zutaten'
newrecipe = False

for infile in infiles:
  ff = open(infile)
  contents = ff.read()
  if 'haupt' in infile:
    print('Hauptgerichte')
  if 'nachspeisen' in infile:
    print('Nachspeisen')
  for line in contents.split('\n'):
    if line == 'REZEPT':
      newrecipe = True
      if title != '':
        print(title)
        print(zutaten)
        print(zubereitung)
        title = ''
        zutaten = []
        zubereitung = []
      continue
    if newrecipe:
      title = line
      newrecipe = False
      continue
    if line == 'Zutaten': 
      mode = 'Zutaten'
      continue
    if line == 'Zubereitung': 
      mode = 'Zubereitung'
      continue
    if mode == 'Zutaten':
      zutaten.append(line)
    if mode == 'Zubereitung':
      zubereitung.append(line)
   
  print(title)
  print(zutaten)
  print(zubereitung)
  title = ''
  zutaten = []
  zubereitung = []
