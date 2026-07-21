#!/usr/bin/python3


import musicbrainzngs
import urllib.request
from urllib.error import HTTPError, URLError
import sys, os

if len(sys.argv) < 3:
  print('not enough arguments')
  print('Argument 1: Artist')
  print('Argument 2: Album')
  sys.exit()

s_artist = sys.argv[1].lower()
s_album  = sys.argv[2].lower()

musicbrainzngs.set_useragent(
    'python-musicbrainzngs-example',
    '0.1',
    'https://github.com/alastair/python-musicbrainzngs/',
)

result = musicbrainzngs.search_artists(artist=s_artist, type='artist')
#for artist in result['artist-list']:
#    print(u"{id}: {name}".format(id=artist['id'], name=artist["name"]))

artist = result['artist-list'][0]
print(u"Found artist!      {id}: {name}".format(id=artist['id'], name=artist['name']))


result = musicbrainzngs.get_artist_by_id(artist['id'],
              includes=["release-groups"], release_type=["album", "ep"])
rg_id = ""
for release_group in result["artist"]["release-group-list"]:
  # print(release_group["title"])
  if s_album == release_group["title"].lower():
    print("Found album!       {title} ({type})".format(title=release_group["title"],
                                    type=release_group["type"]))
    # print(release_group)
    rg_id = release_group['id']




images = musicbrainzngs.get_release_group_image_list(rg_id)

url = ''
candidate = []
for im in images['images']:
  # print(im['approved'])
  print('Image - front: ' + str(im['front']) + '  ---- url: ' + im['image'])
  if str(im['front']) == 'True':
    candidate.append(im['image'])
  if not url:
    url = im['image']

if candidate is not []:
  print(candidate)
  url = candidate[0]

# try:
  # with urllib.request.urlopen(url) as img:
    # with open(filename, 'wb') as outfile:
      # outfile.write(img.read())
# except HTTPError as error:
  # print('no image file')

outfile = s_artist.lower().replace(' ', '_') + '_' + s_album.lower().replace(' ', '_') + '.jpg'
os.system('wget -nv -O ' + outfile + ' ' + url)
