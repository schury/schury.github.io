#!/usr/bin/python3

import urllib.request, sys, os, json
from urllib.error import HTTPError, URLError
from datetime import datetime

test = True

types = {'SelfConsumption' : 0, 'Purchased' : 0, 'Production' : 0, 'Consumption' : 0, 'FeedIn' : 0}
meters = ','.join(types)

# for testing we use a local file containing the api response
outstring = ''
if test:
  f = open('response-2022', 'r')
  outstring = f.readline()
else:
  dateStart = str(datetime.today().year) + '-01-01'
  dateEnd   = '2025-12-31'
  dateEnd   = datetime.today().strftime('%Y-%m-%d')

  infile = open("../../se-api-key", "r")
  api_key = infile.read()

  raw_url = 'https://monitoringapi.solaredge.com/site/3045847/energyDetails?meters=$METERS&timeUnit=MONTH&startTime=$DATESTART%2000:00:00&endTime=$DATEEND%2000:00:00&api_key=$APIKEY'

  url = raw_url.replace('$METERS', meters).replace('$APIKEY', api_key).replace('$DATESTART', dateStart).replace('$DATEEND', dateEnd)

  data = urllib.request.urlopen(url)
  outstring = data.read().decode('UTF-8')

type_header = '          '
lines = []
type_totals = 'Totals:   '
header_length = 0
padding = '   '

j = json.loads(outstring)["energyDetails"]["meters"]

for key in types:
  for i in range(len(types)):
    if key == j[i]["type"]:
      types[key] = i

first = True
for key in types:
  curr_type_index = types[key]
  # print(j[curr_type_index]["type"])
  # print(curr_type_index)
  vals = j[curr_type_index]["values"]
  header_length = len(j[curr_type_index]["type"])
  type_header = type_header + j[curr_type_index]["type"] + padding
  total = 0.0
  k = 0
  for v in vals:
    if first:
      tmp = str(round(v["value"]/1000.0, 1))
      lines.append(v["date"].split()[0][0:-3] + '   ' + tmp.rjust(header_length))
    else:
      lines[k] = lines[k] + str(round(v["value"]/1000.0, 1)).rjust(header_length + len(padding))
    k = k + 1
    total = total + v["value"]
  if first:
    type_totals = type_totals + str(round(total/1000.0, 1)).rjust(header_length)
  else:
    type_totals = type_totals + str(round(total/1000.0, 1)).rjust(header_length + len(padding))
  first = False
    
print(type_header)
for l in lines:
  print(l)
print('-' * len(type_totals))
print(type_totals)

if False:
  with urllib.request.urlopen(url) as data:
    outstring = data.read().decode('UTF-8')
    print(outstring)

    j = json.loads(outstring)
    vals = j["energyDetails"]["meters"][0]["values"]
    for v in vals:
      print(v["date"] + '   ' + str(v["value"]))
