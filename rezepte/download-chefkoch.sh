#!/usr/bin/python3

import urllib.request, sys, os
from urllib.error import HTTPError, URLError

if len(sys.argv) < 2:
  print('need url from chefkoch.de')
  sys.exit()

url = sys.argv[1]

#url = 'https://www.chefkoch.de/rezepte/4285991707060432/Shawarma-Huhn-nach-libanesischer-Art.html'
def download_and_save_recipe(url, outfile):
  out = open(outfile, 'w')
  next_twenty = 0
  print_next_line = False
  try:
    with urllib.request.urlopen(url) as tmp_file:
      contents = tmp_file.read().decode('utf-8').split('\n')
      
      for line in contents:
        if '"Recipe"' in line:
          out.write(line)
          next_twenty += 1
          continue
        if next_twenty > 0:
          if print_next_line:
            out.write(line)
            print_next_line = False
            continue
          if '"description"' in line:
            out.write(line)
          if '"recipeIngredient"' in line:
            out.write(line)
            print_next_line = True
          if '"recipeInstructions"' in line:
            out.write(line)
          if '"name"' in line:
            out.write(line)
          next_twenty += 1
        if next_twenty > 30:
          break
  except HTTPError as error:
    print('could not download webpage')
  except URLError as error:
    print('could not download webpage')



download_and_save_recipe(url, 'tmp_recipe')
