#!/usr/bin/python3

import subprocess
import requests
import re
import os
import sys
import psutil
import time
import wave
import glob
from mutagen.flac import FLAC
from mutagen.easyid3 import EasyID3
import cdio
import pycdio

Debug = False

if len(sys.argv) > 1:
  print('Enable testing mode')
  print('WARNING: testing doesn\'t work anymore!!')
else:
  print('Converting CD...')
  


dir_temp_rip = os.getcwd() + '/temp-rip'
dir_idcache = os.getcwd() + '/cddb-cache'


class Track:
  def __init__(self, num, name):
    self.number = "{:02d}".format(num)
    self.name   = name.strip()
  def __str__(self):
    return self.number + ' - ' + self.name
  number = 0
  name   = ''



# only valid for linux, probably
CD_OFFSET=150
CD_FRAMES=75

def cddb_sum(n):
  ret = 0
  while(n > 1):
    ret += int(n % 10)
    n /= 10
  return ret

def calculate_checksum():
  try:
    d = cdio.Device(driver_id=pycdio.DRIVER_UNKNOWN)
    drive_name = d.get_device()
  except IOError:
    print("Problem finding a CD-ROM")
    sys.exit(1)

  t = d.get_first_track()
  if t is None:
      print("Problem getting first track")
      sys.exit(2)

  first_track = t.track
  num_tracks  = d.get_num_tracks()
  last_track  = first_track+num_tracks

  check_sum=0
  i = first_track
  prev_lsn = 0
  tracks_string = " "
  while(i < last_track):
    t1 = d.get_track(i)
    check_sum += cddb_sum((CD_OFFSET+t1.get_lsn())/CD_FRAMES)
    tracks_string += str(CD_OFFSET+t1.get_lsn()) + " "
    i += 1
    prev_lsn = t1.get_lsn()

  #print("%3X: %06lu  leadout" % (pycdio.CDROM_LEADOUT_TRACK, d.get_disc_last_lsn()))

  totaltime = int( (d.get_disc_last_lsn() - d.get_first_track().get_lsn())/CD_FRAMES )


  #print("Checksum: " + str(check_sum))
  #print("Total time: " + str(totaltime))


  cs = ("%08lx " % ((check_sum % 0xff) << 24 | totaltime << 8 | num_tracks))

  return cs + str(num_tracks) + tracks_string + str(int( (d.get_disc_last_lsn() + CD_OFFSET )/CD_FRAMES ))



def call_cdparanoia(num_tracks):
  os.chdir(dir_temp_rip)
# -B batch mode, save each track in a separate file
# -l log to cdparanoia.log
# -q quiet
# -Z disable paranoia - for scratched cds
  command = '/usr/bin/cdparanoia -B -l -q -Z'
  command = '/usr/bin/cdparanoia -B -l -q'
  if Debug:
    print("cdparanoia command:")
    print(command)
  pid = subprocess.Popen(command, shell=True).pid
  print('Extraction progress:')
  while psutil.pid_exists(pid):
    time.sleep(1)
    # read log file, but remove last character which is a line break
    output = os.popen('tail -n 1 cdparanoia.log').read()[0:-1]
    with open('cdparanoia.log') as file:
      contents = file.read()
      last_line = contents.splitlines()[-1]
      if 'track' in last_line:
        # overwrite the end of the string with blanks, as the first string is longer that the other ones
        print(' ', last_line + ' / Total: ' + str(num_tracks), sep='', end='\r', flush=True)
  # print a newline at the end of extraction
  print('')



def call_flac():
  print('Converting tracks to flac...')
  os.chdir(dir_temp_rip)
  # print(os.getcwd())
  tracks = []
  pids = []
  for l in open(dir_temp_rip + '/cdparanoia.log'):
    if 'outputting' in l:
      tracks.append(l.split()[2])

  for t in tracks:
    # subprocess.call('flac ' + t, shell=True)
    pid = subprocess.Popen('flac -s ' + t, shell=True).pid
    pids.append(pid)

  for p in pids:
    if psutil.pid_exists(p):
      time.sleep(0.05)
    else:
      pids.remove(p)



def tag_and_rename_flac_files(cd_id):
  os.chdir(dir_temp_rip)
# read tags from cddb-file
  cd_artist = ''
  cd_album  = ''
  cd_year   = ''
  cd_genre  = ''
  tracks    = []
  num       = 0
  for l in open(dir_idcache + '/' + cd_id):
    s = l.split('=')
    if s[0] == 'Dtitle':
      cd_artist = s[1].split('/')[0].strip()
      cd_album  = s[1].split('/')[1].strip()
    if s[0] == 'Dyear':
      cd_year = s[1].strip()
    if s[0] == 'Dgenre':
      cd_genre = s[1].strip()
    if s[0][:6] == 'Ttitle':
      num = num + 1
      tracks.append(Track(num, s[1]))

  # print(cd_artist, cd_album, cd_year, cd_genre, num)

  dir_target = cd_artist + ' - [' + cd_year + '] ' + cd_album
  if os.path.isdir(dir_target):
    print('WARNING: target directory already exists. Error? ' + dir_target)
  else:
    os.mkdir(dir_target)

  for t in tracks:
    # print(t)
    flac_name = 'track' + t.number + '.cdda.flac'
    # we need to check here if the file actually exists
    # data tracks will not be extracted, so this doesn't have to be an error...
    if os.path.exists(flac_name):
      audio = FLAC(flac_name)
      audio['ARTIST'] = cd_artist
      audio['ALBUM']  = cd_album
      audio['TITLE']  = t.name
      audio['DATE']   = cd_year
      audio['GENRE']  = cd_genre
      audio['TRACKNUMBER'] = t.number
      audio['TRACKTOTAL']  = str(num)
      audio['CDDB']   = cd_id
      audio.save()

      os.rename(flac_name, dir_target + '/' + str(t) + '.flac')
    else:
      print('WARNING: file ' + flac_name + ' doesn\'t exist. Maybe a data track?')

  
def create_mp3():
  print('converting tracks to MP3...')
  os.chdir(dir_temp_rip)

# read tags from cddb-file
  cd_artist = ''
  cd_album  = ''
  cd_year   = ''
  cd_genre  = ''
  for l in open(dir_idcache + '/' + cd_id):
    s = l.split('=')
    if s[0] == 'Dtitle':
      cd_artist = s[1].split('/')[0].strip()
      cd_album  = s[1].split('/')[1].strip()
    if s[0] == 'Dyear':
      cd_year = s[1].strip()
    if s[0] == 'Dgenre':
      cd_genre = s[1].strip()

  mp3_filename = cd_artist + ' - [' + cd_year + '] ' + cd_album + '.mp3'

# join the wav files together using python wave
# os.system('shntool join -q -O always -n track*.wav') 
  infiles = glob.glob('track*.wav', recursive=True)
  infiles.sort()
  # print(infiles)
  outfile = "joined.wav"


  data = []
  for infile in infiles:
      w = wave.open(infile, 'rb')
      data.append( [w.getparams(), w.readframes(w.getnframes())] )
      w.close()
      
  output = wave.open(outfile, 'wb')
  output.setparams(data[0][0])
  for i in range(len(data)):
      output.writeframes(data[i][1])
  output.close()


  os.system('ffmpeg -loglevel warning -i joined.wav -acodec mp3 -ab 128k out.mp3')  
  os.rename('out.mp3', mp3_filename)
# alternative for ffmpeg conversion using lame - maybe higher quality?
# lame -h joined.wav

# potential alternative for joining and converting in one step, instead of first joining and afterwards converting
# may introduce some gaps!
# ffmpeg -i track01.cdda.wav -i track02.cdda.wav -i track03.cdda.wav -i track04.cdda.wav -i track05.cdda.wav -filter_complex "concat=n=5:v=0:a=1" -vn -y -acodec mp3 -ab 128k out3.mp3


  audio = EasyID3(mp3_filename)
  audio['artist'] = cd_artist
  audio['album']  = cd_album
  audio['title']  = cd_album
  audio['genre']  = cd_genre
  audio['date']   = cd_year
  audio.save()
  


def cleanup(cd_id):
  print('cleaning up...')
  os.chdir(dir_temp_rip)
  os.mkdir(cd_id)
  os.system('mv track*.wav joined.wav cdparanoia.log ' + cd_id)






def parse_and_print_cddb_result(cddb_read):
  result = []
  first = True
  for i in cddb_read.split('\r\n'):
    if first:
      print(i)
      first = False
    if len(i) < 2:
      continue
# we only want the lines starting with D or T
    if i[0] == 'D' or i[0] == 'T':
# we want to have all words starting with a capital letter
      r = i.title()
# the discid should stay in the original format though...
      if r[0:6] == 'Discid':
        r = 'Discid=' + cd_id
      if r[0:6] == 'Dgenre':
        genre = r.split('=')[1]
        if genre == 'Metal':
          r = 'Dgenre=Heavy Metal'
# if there's an apostrophe ' after a word, we want the next letter to be lowercase
      if '\'' in r:
        j = r.find('\'')
        r = r[:j+1] + r[j+1].lower() + r[j+2:]
# if there is a slash / in the trackname, we have to substitute
      if r[0] == 'T':
        r = r.replace("/", "-")
        r = r.replace("[", "(")
        r = r.replace("]", ")")
        r = r.replace("Ii", "II")
        r = r.replace("Iii", "III")
      result.append(r)

  r = '\n'.join(result)
  return r


def query_cddb_and_select_result(disc_id):
# query cddb if the cd exists in the database
# gnudb.org works like this:
# step 1: query 
#   query needs disc_id and track offsets
# step 2: read
#   read needs only the discid and the genre
# to_check: if the result is unique, we directly receive the read result?
  query = 'https://gnudb.gnudb.org/~cddb/cddb.cgi?cmd=cddb+query+' + disc_id.replace(' ', '+') + '&hello=misty+yahoo.com+selfmade+0.1&proto=6'
  if Debug:
    print("query command:")
    print(query)
  cddb_query_result = requests.get(query).text

  print('CDDB query result: ' + cddb_query_result)

# here we may get multiple results; we need to select one of those
  lines = cddb_query_result.splitlines()
  cd_cat_index = 1
  cd_id_index  = 2

  for line in lines:
    if line.split()[0] == '210':
      cd_cat_index = 0
      cd_id_index  = 1
      print('CDDB: multiple results:')
      continue
    if line.split()[0] == '211':
      cd_cat_index = 0
      cd_id_index  = 1
      print('CDDB: inexact results found:')
      continue
    if line == '.':
      continue
    if line.split()[0] == '200':
      print('CDDB: exactly one result found:')

    s = line.split(' ')
    cd_category = s[cd_cat_index]
    cd_id       = s[cd_id_index]

    query2 = 'https://gnudb.gnudb.org/~cddb/cddb.cgi?cmd=cddb+read+' + cd_category + '+' + cd_id + '&hello=misty+yahoo.com+selfmade+0.1&proto=6'
    cddb_read = requests.get(query2).text
    cddb_read = parse_and_print_cddb_result(cddb_read)
    cddb_results.append(cddb_read)
    if Debug:
      print("  cddb_read result:")
      print(cddb_read)

# find the separator '/' in the list of tokens
# use it later for artist and title separation
  ind = 0
  l = 3
  while l < len(s):
    if s[l] == '/':
      ind = l
      break
    l = l + 1
  if len(lines) > 2:
    val = int(input("Choose entry: ") or "0") - 1
    #print("You selected entry number " + str(val))
    cddb_read = cddb_results[val]

  return cddb_read










##########
#  MAIN  #
##########

cddb_query_result = ''
cddb_results = []
cd_category = ''
cd_id       = ''
disc_id = ''


# use external program cd-discid to get the discid
# DEP remove this dependency by calculating from scratch?
#disc_id = subprocess.getoutput('cd-discid')
disc_id = calculate_checksum()
if 'CDROMREADTOCHDR' in disc_id:
  print('Error: ' + disc_id)
  sys.exit()

print('DiscID: ' + disc_id)

cd_id = disc_id.split()[0]

cache_filename = dir_idcache + '/' + cd_id
# print(cache_filename)



# check if we had this cd before and use the old cddb-file if so
# otherwise, make a request to cddb and get the information
if os.path.isfile(cache_filename):
  # read cddb information from file
  with open(cache_filename) as f:
    cddb_read = f.read()
else:
  cddb_read = query_cddb_and_select_result(disc_id)
  with open(cache_filename, 'w') as f:
    f.write(cddb_read)

  # now that we have everything, start up a GUI to edit the file
  subprocess.call("vim " + cache_filename, shell=True)





# print the contents of the cache_file so we see the data
cd_tracks = 0
with open(cache_filename) as infile:
  contents = infile.read()
  for l in contents.splitlines():
    print(l)
    if l and l[0] == 'T':
      cd_tracks += 1
    s = l.split('=')
    if s[0] == 'Dtitle':
      aa = s[1].split(' / ')
      cd_artist = aa[0]
      cd_album  = ' '.join(aa[1:])

print(' ID: ' + cd_id + ' / #tracks: ' + str(cd_tracks) + ' / Artist: ' + cd_artist + ' / Album: ' + cd_album)

# finally call cdparanoia to rip the cd contents
call_cdparanoia(cd_tracks)

call_flac()

tag_and_rename_flac_files(cd_id)

# we can eject the cd, everything is finished
os.system('eject')

create_mp3()
cleanup(cd_id)
