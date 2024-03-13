#!/usr/bin/python3

import urllib.request, sys, os

from PIL import Image
import PIL

# creating a image object (main image)
# im1 = Image.open(r"C:\Users\System-Pc\Desktop\flower1.jpg")

# save a image using extension
# im1 = im1.save("geeks.jpg")
def download_and_save_art(rg_id, filename):
  url = 'https://coverartarchive.org' + rg_id + '/front'

  with urllib.request.urlopen(url) as img:
    print(img)
    with open(filename, 'wb') as outfile:
      outfile.write(img.read())
    # bla = Image(img).save('test.jpg')

relgroup_id = '0519b1bf-c443-3110-8fb0-6fbbf8f3862b'


def get_cd_list():
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

  return cdlist



cdlist = get_cd_list()
old_artist = ''
artist_cd_list = []
first = True
for cd in cdlist:
  artist = cd.split(' - ')[0].lower()
  album =  ' '.join(cd.split(']')[1:]).strip()

  if artist != old_artist:
    if first: 
      first = False
    else:
      # sys.exit()
      first = False
    old_artist = artist
    searchstring = artist.replace(' ', '+')
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
                artist_cd_list.append(temp + ' ' + s.title())
                temp = ''
              if ('/release-group/' in c) and not ('http' in c):
                temp = c
                print_next = True



    # print(artist_cd_list)

  for c in artist_cd_list:
    if album in c:
      # print('found album ' + album + ' of artist ' + artist + ' in cd-list!')
      filename = artist.lower().replace(' ', '_') + '_' + album.lower().replace(' ', '_') + '.jpg'
      rg_id = c.split()[0]
      print(rg_id + ' ----- ' + filename)
      if not os.path.isfile(filename):
        print(' downloading file...')
        download_and_save_art(rg_id, filename)
      else:
        print(' file already downloaded, skipping!')

          

