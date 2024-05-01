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

def print_recipe(title, zutaten, zubereitung):
  print(rez_header.replace('TITLE', title))
  print('Zutaten')
  print(zutaten)
  print('Zubereitung')
  print(zubereitung)

title = ''
zutaten = []
zubereitung = []

infiles = ['rezepte/hauptgerichte.txt', 'rezepte/nachspeisen.txt']

mode = 'zutaten'
newrecipe = False
recipe_html = []

for infile in infiles:
  ff = open(infile)
  contents = ff.read()
  if 'haupt' in infile:
    print('Hauptgerichte')
  if 'nachspeisen' in infile:
    print('Nachspeisen')
  for line in contents.split('\n'):
    if line == '':
      continue
    if line == 'REZEPT':
      newrecipe = True
      if title != '':
        print_recipe(title, zutaten, zubereitung)
        recipe_html.append(title)
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
   
  print_recipe(title, zutaten, zubereitung)
  recipe_html.append(title)
  title = ''
  zutaten = []
  zubereitung = []
  print(recipe_html)
  recipe_html = []

