#!/usr/bin/python3

import urllib.request, sys, os, json
from urllib.error import HTTPError, URLError

types = ['Production', 'Consumption', 'SelfConsumption', 'FeedIn', 'Purchased']
meters = ','.join(types)

infile = open("../../se-api-key", "r")
api_key = infile.read()

raw_url = 'https://monitoringapi.solaredge.com/site/3045847/energyDetails?meters=$METERS&timeUnit=MONTH&startTime=2025-01-01%2000:00:00&endTime=2025-07-31%2000:00:00&api_key=$APIKEY'

url = raw_url.replace('$METERS', meters).replace('$APIKEY', api_key)

# for testing we use a local file containing the api response
f = open('response', 'r')
outstring = f.readline()

for i in range(len(types)):
  j = json.loads(outstring)["energyDetails"]["meters"]
  vals = j[i]["values"]
  print(j[i]["type"])
  total = 0.0
  for v in vals:
    print(v["date"].split()[0] + '   ' + str(round(v["value"]/1000.0, 1)))
    total = total + v["value"]
  print("Total: " + str(total/1000.0))
    


if False:
  with urllib.request.urlopen(url) as data:
    outstring = data.read().decode('UTF-8')
    print(outstring)

    j = json.loads(outstring)
    vals = j["energyDetails"]["meters"][0]["values"]
    for v in vals:
      print(v["date"] + '   ' + str(v["value"]))
