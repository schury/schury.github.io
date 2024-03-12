#!/usr/bin/python3

import urllib.request, sys

from PIL import Image
import PIL

# creating a image object (main image)
# im1 = Image.open(r"C:\Users\System-Pc\Desktop\flower1.jpg")

# save a image using extension
# im1 = im1.save("geeks.jpg")
def download_and_save_art(rg_id):
  url = 'https://coverartarchive.org/release-group/' + rg_id + '/front'

  with urllib.request.urlopen(url) as img:
    print(img)
    with open('out.jpg', 'wb') as outfile:
      outfile.write(img.read())
    # bla = Image(img).save('test.jpg')

relgroup_id = '0519b1bf-c443-3110-8fb0-6fbbf8f3862b'


# use cd-list-raw-length as input for getting artist and album
cdlistcontent = '' 
with open('../cd-list-raw-length') as cdlist:
  cdlistcontent = cdlist.read()

lastline = ''
cdlist = []
for line in cdlistcontent.splitlines():
  l = line.split('/')[0]
  l = l.replace(' (Bonus)', '')
  l = l.replace(' (Bonus Instrumental)', '')
  l = l.replace(' (CD 1)', '')
  l = l.replace(' (CD 2)', '')
  if l == lastline:
    continue
  lastline = l
  cdlist.append(l)


for cd in cdlist:
  artist = cd.split(' - ')[0]
  album =  ' '.join(cd.split(']')[1:]).strip()
  print(artist + ' --- ' + album)
  


sys.exit()

artist = 'bolt+thrower+honour+-+valour+-+pride'
with urllib.request.urlopen('https://musicbrainz.org/search?query=' + artist + '&type=artist&limit=1&method=indexed') as artist_list:
  html_artist = str(artist_list.read()).split('\"')
  for h in html_artist: 
    if '/artist/' in h:
      artist_id = (h.split('/')[2])
      # print(artist_id)
      with urllib.request.urlopen('https://musicbrainz.org/artist/' + artist_id) as cd_list:
        html_cds = str(cd_list.read()).split('\"')
        for c in html_cds:
          if ('/release-group/' in c or 'bdi' in c) and not ('http' in c):
            print(c)

