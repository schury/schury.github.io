#!/usr/bin/python3

import urllib.request, sys, os, re
from urllib.error import HTTPError, URLError

recipe_name = ''
recipe_instructions = ''

def sanitize_line(l):
  l = l.replace('½', '1/2')
  l = l.replace('¼', '1/4')
  while '  ' in l:
    l = l.replace('  ', ' ')
  return l

if len(sys.argv) < 2:
  print('need url from chefkoch.de')
  sys.exit()

url = sys.argv[1]

#url = 'https://www.chefkoch.de/rezepte/4285991707060432/Shawarma-Huhn-nach-libanesischer-Art.html'
def download_and_parse_recipe(url):
  next_twenty = 0
  name_done = False
  print_next_line = False
  try:
    with urllib.request.urlopen(url) as tmp_file:
      contents = tmp_file.read().decode('utf-8').split('\n')
      #contents = tmp_file.read().decode('unicode_escape').split('\n')
      
      for line in contents:
        #line = sanitize_line(line)
        if '"Recipe"' in line:
          next_twenty += 1
          continue
        if next_twenty > 0:
          if print_next_line:
            recipe_ingredients = sanitize_line(line.encode('utf-8').decode('unicode_escape'))
            recipe_ingredients = '\n'.join(x.replace('"','').replace(' ,', ',').replace('],','').strip() for x in recipe_ingredients.split('", "'))
            print_next_line = False
            continue
          if '"recipeIngredient"' in line:
            print_next_line = True
          if '"recipeInstructions"' in line:
            recipe_instructions = line.split(':')[1][2:].encode('utf-8').decode('unicode_escape')
          if '"name"' in line and not name_done:
            name_done = True
            recipe_name = line.split(':')[1][2:-2].encode('utf-8').decode('unicode_escape')
          next_twenty += 1
        if next_twenty > 30:
          break
  except HTTPError as error:
    print('could not download webpage')
  except URLError as error:
    print('could not download webpage')

  return recipe_name, recipe_ingredients, recipe_instructions


recipe_name, recipe_ingredients, recipe_instructions = download_and_parse_recipe(url)

print('REZEPT')
print(recipe_name)
print('Zutaten\n' + recipe_ingredients)
print('Zubereitung\n' + recipe_instructions.replace('",','') + '\n')
