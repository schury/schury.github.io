#!/usr/bin/python3

import os, sys
from datetime import date

stopat = 50000
c = 0
num_real = 1
num_disp = 1
album_l  = 0
song_list = []

covers_found = 0

def write_cd_header(file):
  header = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CD list</title>
  <link rel="stylesheet" href=\"../css/cds.css\">
</head>
<body>
<h1>CD list</h1>
<table>
<thead><tr><th>#</th><th>Artist</th><th>Album</th><th>Year</th></tr></thead>
<tbody>
'''

  file.write(header)


def write_songs_to_file(num, artist, album, year, songs, album_length):
  global covers_found
  header = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>CD-Liste</title>
  <link rel="stylesheet" href="../../css/cds.css">
</head>
<body>
'''.replace('CD-Liste', album)
  outfile = open('songs/' + num + '.html', "w")
  outfile.write(header)
  outfile.write('<h1>' + artist + '</h1>\n')
  outfile.write('<h2>' + album + ' - ' + year + '</h2>\n')
  outfile.write('<table>\n')
  outfile.write('<thead><tr><th>#</th><th>Title</th><th>Length</th></tr></thead>\n')
  outfile.write('<tbody>\n')
  outfile.write('\n'.join(songs))
  outfile.write('\n<tr class="last"><td></td><td>Total:</td><td>' + album_length + '</td></tr>\n')
  outfile.write('</tbody>\n')
  outfile.write('</table>\n')
  # check for album art and add if available
  art_filename = 'albumart/' + artist.lower().replace(' ', '_') + '_' + album.lower().replace(' ', '_') + '.jpg'
  art_filename = art_filename.replace('_(bonus)', '').replace('_(bonus_instrumental)', '')
  # print(art_filename)
  if os.path.isfile(art_filename):
    outfile.write('<img src="../' + art_filename + '" alt="cover not found" />\n')
    covers_found += 1
  else:
    print(art_filename + ' cover not found')
  outfile.write('</body>\n')

outfilename = "index.html"
if os.path.isfile(outfilename):
  os.remove(outfilename)
outfile = open(outfilename, "a")
write_cd_header(outfile)

infile = open("cd-list-raw-length")
contents = infile.read()
for line in contents.split("\n"):
  if line == '':
    continue
  ls = line.split("/")

  c += 1
  if c == stopat:
    print('\n'.join(song_list))
    sys.exit()

  # artist, album and year can be updated only after we wrote the old songs out to file
  sss    = ls[0].split('[')
  song_n = ls[1][0:2]
  song_t = ls[1][5:].strip()
  song_length = (int(ls[2]) / 44100)
  min = int(song_length / 60)
  sec = int(song_length % 60)
  song_l = f'{min:02}' + ':' + f'{sec:02}'

  if song_n == "01":
    # we have a new album, so we must output the last album
    if song_list != []:
      write_songs_to_file(f'{num_real:03}', artist, album, year, song_list, f'{int(album_l / 60):02}' + ':' + f'{int(album_l % 60):02}')
      num_real += 1
      song_list = []
    artist = sss[0][0:-3]
    year   = sss[1][0:4]
    album  = sss[1][6:]
    if ("(Bonus)" in album) or ("(CD 2)" in album) or ("(Bonus Instrumental)" in album):
      outfile.write('<tr><td></td><td>' + artist + '</td><td><a href=\"songs/' + f'{num_real:03}' + '.html\">' + album + '</a></td><td>' + year + '</td></tr>\n')
    else:
      outfile.write('<tr><td>' + f'{num_disp:03}' + '</td><td>' + artist + '</td><td><a href=\"songs/' + f'{num_real:03}' + '.html\">' + album + '</a></td><td>' + year + '</td></tr>\n')
      num_disp += 1

    # afterwards, we save for new album
    album_l  = min * 60 + sec
  else:
    album_l += min * 60 + sec

  song_list.append('<tr><td>' + song_n + '</td><td>' + song_t + '</td><td>' + song_l + '</td></tr>')


write_songs_to_file(f'{num_real:03}', artist, album, year, song_list, f'{int(album_l / 60):02}' + ':' + f'{int(album_l % 60):02}')
outfile.write('</tbody>\n</table>\n<br>\n')
outfile.write('Created: ' + str(date.today()) + '\n')
outfile.write('</body>\n')

print('found ' + str(covers_found) + ' covers')
