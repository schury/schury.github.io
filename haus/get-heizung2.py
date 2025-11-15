#!/usr/bin/python3

##### TODO
## - anhängen aktueller Stand an pellets datei

import requests, time
from datetime import datetime

url  = 'http://192.168.178.26:8080/user/vars/messwerte'

r = requests.get(url)
for l in r.text.splitlines():
  print(l)
