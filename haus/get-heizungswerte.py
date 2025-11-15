#!/usr/bin/python3

##### TODO
## - anhängen aktueller Stand an pellets datei

import requests, time
from datetime import datetime

url_amount_storage  = 'http://192.168.178.26:8080/user/var/264/10201/0/0/12015'
url_amount_internal = 'http://192.168.178.26:8080/user/var/264/10891/0/0/12011'
url_tries           = 'http://192.168.178.26:8080/user/var/264/10891/0/0/14560'

storage  = 0
internal = 0
tries    = 0

r = requests.get(url_amount_storage)
for l in r.text.splitlines():
  if 'strValue' in l:
    storage = int(l.split()[4].split('"')[1])

r = requests.get(url_amount_internal)
for l in r.text.splitlines():
  if 'strValue' in l:
    internal = int(l.split()[4].split('"')[1])

r = requests.get(url_tries)
for l in r.text.splitlines():
  if 'strValue' in l:
    tries = l.split()[4].split('"')[1]

date_now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
outstring = "{:04d}".format(storage + internal) + 'kg ' + date_now + ' ' + tries

with open('pellets', 'a') as file:
  file.write(outstring + '\n')

header_text = ['Durchschnitt (pro Tag)', ' Tage', '      Verbrauch', 'Zeitraum               ', 'Retouren']
    
pellets_file = open('pellets')
lines = pellets_file.readlines()[-20:]

first = True
for l in lines:
  if first:
    pellets_old = int(l.split()[0][0:-2])
    date_old = datetime.strptime(l.split()[1] + ' ' + l.split()[2], "%d.%m.%Y %H:%M:%S")
    print(' '.join(header_text))
    first = False
    continue
  p = int(l.split()[0][0:-2])
  d = datetime.strptime(l.split()[1] + ' ' + l.split()[2], "%d.%m.%Y %H:%M:%S")
  t = l.split()[3]
  d_diff = d - date_old
  p_diff = pellets_old - p
  if p_diff < 0:
    print('TANKEN ' + str(-1*p_diff))
    pellets_old = p
    date_old = d
    continue
  secs = d_diff.total_seconds()
  avg_pellets = 24*3600 * (p_diff / secs)
  hoursmins = time.strftime("%H:%M", time.gmtime(secs))
  days = int(d_diff.days)
  print("{:22.2f} {:5d}d {:8s} {:5d} {} {}".format(avg_pellets, days, hoursmins, p_diff, date_old.strftime("%d.%m.%Y") + ' - ' + d.strftime("%d.%m.%Y"), t))


  pellets_old = p
  date_old = d
