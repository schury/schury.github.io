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
<h1>Rezepte</h1>
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

def write_recipe_headers(out, recipe_html):
  out.write('<ul>\n')
  for i in recipe_html:
    out.write('<li>' + i + '</li>\n')
  out.write('</ul>\n')

title = ''
zutaten = []
zubereitung = []

infiles = ['rezepte/hauptgerichte.txt', 'rezepte/nachspeisen.txt']

mode = 'zutaten'
newrecipe = False
recipe_html = []

rez_html_out = open('rezepte.html', 'w')
rez_html_out.write(main_header)

for infile in infiles:
  ff = open(infile)
  contents = ff.read()
  if 'haupt' in infile:
    rez_html_out.write('<h2>Hauptgerichte</h2>\n')
  if 'nachspeisen' in infile:
    rez_html_out.write('<h2>Nachspeisen</h2>\n')
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
  write_recipe_headers(rez_html_out, recipe_html)
  recipe_html = []

rez_html_out.write('</body>')
