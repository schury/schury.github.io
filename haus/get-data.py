#!/usr/bin/python3

import urllib.request, sys, os
from urllib.error import HTTPError, URLError

types = ['Production', 'Consumption', 'SelfConsumption', 'FeedIn', 'Purchased']

infile = open("../../se-api-key", "r")
api_key = infile.read()

raw_url = 'https://monitoringapi.solaredge.com/site/3045847/energyDetails?meters=$MM&timeUnit=MONTH&startTime=2025-01-01%2000:00:00&endTime=2025-07-31%2000:00:00&api_key=$APIKEY'

url = raw_url.replace('$APIKEY', api_key)

for t in types:
  u = url.replace('$MM', t)
  with urllib.request.urlopen(u) as data:
    outstring = data.read().decode('UTF-8')
    print(outstring)
    values = outstring.split('"values":')[1].split('},{')
    for v in values: 
      print(v)
