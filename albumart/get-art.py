#!/usr/bin/python3

import urllib.request, sys, os
from urllib.error import HTTPError, URLError

from PIL import Image
import PIL

# creating a image object (main image)
# im1 = Image.open(r"C:\Users\System-Pc\Desktop\flower1.jpg")

# save a image using extension
# im1 = im1.save("geeks.jpg")
def download_and_save_art(rg_id, filename):
  url = 'https://coverartarchive.org' + rg_id + '/front'

  try:
    with urllib.request.urlopen(url) as img:
      # print(img)
      with open(filename, 'wb') as outfile:
        outfile.write(img.read())
      # bla = Image(img).save('test.jpg')
  except HTTPError as error:
    print('no image file')



if len(sys.argv) < 3:
  print('not enough arguments')
  sys.exit()

artist = sys.argv[1].lower()
album  = sys.argv[2].lower()

#artist = 'Witchery'
#album =  'Nightside'

filename = artist.lower().replace(' ', '_') + '_' + album.lower().replace(' ', '_') + '.jpg'

if os.path.isfile(filename):
  print(filename + ' already downloaded, skipping!')
  sys.exit()

artist_cd_list = []
searchstring = artist.replace(' ', '+').replace('ö', 'o').replace('ÿ', 'y')
with urllib.request.urlopen('https://musicbrainz.org/search?query=' + searchstring + '&type=artist&limit=1&method=indexed') as artist_list:
  html_artist = str(artist_list.read()).split('\"')
  for h in html_artist: 
    if '/artist/' in h:
      artist_id = (h.split('/')[2])
      # print(artist_id)
      temp = ''
      with urllib.request.urlopen('https://musicbrainz.org/artist/' + artist_id) as cd_list:
        html_cds = str(cd_list.read()).split('\"')
        print_next = False
        for c in html_cds:
          if print_next:
            print_next = False
            s = c.replace('><bdi>', '')
            s = s[0:s.find('<')]
            s = s.replace('\\xe2\\x80\\xa6', '...')
            s = s.replace('\\xe2\\x80\\x93', '-')
            s = s.replace('\\303\\244', 'ä')
            s = s.replace('\\303\\266', 'ö')
            s = s.replace('\\xc3\\xbc', 'ü')
            artist_cd_list.append(temp + ' ' + s.lower())
            temp = ''
          if ('/release-group/' in c) and not ('http' in c):
            temp = c
            print_next = True



print(artist_cd_list)

# should check the file on the disk first, only then try to download again!
album_found = False
for c in artist_cd_list:
  if album in c:
    print('found album ' + album + ' of artist ' + artist + ' in cd-list!')
    rg_id = c.split()[0]
    print(rg_id + ' ----- ' + filename)
    album_found = True
    if not os.path.isfile(filename):
      print(' downloading file...')
      download_and_save_art(rg_id, filename)

if not album_found:
  print('    -----> ' + artist + ' ' + album + ' not found')

