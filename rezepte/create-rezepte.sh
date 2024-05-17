#!/usr/bin/python3

import os, sys, hashlib
from datetime import date

main_header = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Rezepte</title>
  <link rel="stylesheet" href=\"../css/rezepte.css\">
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


def print_recipe(title, zutaten, zubereitung, num):
  out = open(num + '.html', 'w')
  out.write(rez_header.replace('TITLE', title))
  out.write('<h1>' + title + '</h1>\n')
  out.write('<div class="column">\n<div class="column left">\n')
  out.write('<h2>Zutaten</h2>\n<ul>\n')
  for l in zutaten:
    out.write('<li>' + l + '</li>\n')
  out.write('</ul>\n</div>\n<div class="column right">\n<h2>Zubereitung</h2>\n<ul>\n')
  for l in zubereitung:
    out.write('<li>' + l + '</li>\n')
  out.write('<ul>\n</div>\n</div>\n</body>\n')

def write_recipe_headers(out, recipe_html, recipe_num):
  out.write('<ul>\n')
  i = 0
  while i < len(recipe_html):
    out.write('<li><a href="' + recipe_num[i] + '.html">' + recipe_html[i] + '</a></li>\n')
    i += 1
  out.write('</ul>\n')

title = ''
zutaten = []
zubereitung = []
rez_num = 0

infiles = ['hauptgerichte.txt', 'nachspeisen.txt']

mode = 'zutaten'
newrecipe = False
recipe_html = []
recipe_num = []

rez_html_out = open('index.html', 'w')
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
        rez_num += 1
        rez_html_filename = hashlib.sha256((title + 'rezept').encode('utf-8')).hexdigest()[0:12]
        print_recipe(title, zutaten, zubereitung, rez_html_filename)
        recipe_html.append(title)
        recipe_num.append(rez_html_filename)
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
   
  rez_num += 1
  rez_html_filename = hashlib.sha256((title + 'rezept').encode('utf-8')).hexdigest()[0:12]
  print_recipe(title, zutaten, zubereitung, rez_html_filename)
  recipe_html.append(title)
  recipe_num.append(rez_html_filename)
  title = ''
  zutaten = []
  zubereitung = []
  write_recipe_headers(rez_html_out, recipe_html, recipe_num)
  recipe_html = []
  recipe_num = []

rez_html_out.write('Stand: ' + str(date.today()) + '\n')
rez_html_out.write('</body>')
