#!/usr/bin/python

import requests, json
from datetime import datetime

url = "https://1heiz-pellets.de/x_preis.php"

# data_full = { "Produkt": "P101", "Einheit": "kg", "Transport": "Lieferung", "NettoOnlinerabatt": "0", "NettoPreiszuschlagSchlauch": "30", "formURL": "/preise_holzpellets.php", "Mehrwertsteuerfaktor": "1.07", "Mindestmenge": "3000", "NettoEinblaspauschale": "33", "anti_csrf_token": "697c98f324473", "Lieferzeit": "30", "device": "c", "NettoEinzelpreis": "", "NettoEinzelpreisMindestmenge": "", "Bundesland": "BY", "Fahrzeit": "75", "Gebiet": "", "Lager": "", "Lager_id": "", "NettoPreiszuschlagTermin": "", "Gesamtmenge": "", "Lieferfrist": "", "Kundennummer": "", "GesamtPreisManuell": "", "NettoEinblaspauschaleManuell": "33", "KundenBestellnr": "", "Land": "DE", "Notiz": "", "plz": "91086", "menge": "3000", "lieferstellen": "1", "Auftragsnummer": "", "plzLieferanschrift": "91086", "ortLieferanschrift": "Aurachtal", "anrede": "Herr", "vorname": "", "name": "", "firma": "", "firma2": "", "firma3": "", "anschrift": "", "email": "", "telefon1": "", "telefon2": "", "teilmenge": "", "Rabattmarken": "", "schlauch": "30", "Hinweistext": "", "ara": "nein", "RaVorname": "", "RaName": "", "RaFirma": "", "RaFirma2": "", "RaFirma3": "", "RaAnschrift": "", "RaPLZ": "", "RaOrt": "", "RaEmail": "", "RaTelefon1": "", "RaTelefon2": "", "za": "Vorkasse", "Kontoinhaber": "", "iban": "", "bic": "", "bday": "", "bmonth": "", "byear": "", "GebDatum": "", "Zahlungsbetrag": "", "MontagStart": "0800", "MontagEnde": "1400", "DienstagStart": "0800", "DienstagEnde": "1400", "MittwochStart": "0800", "MittwochEnde": "1400", "DonnerstagStart": "0800", "DonnerstagEnde": "1400", "FreitagStart": "0800", "FreitagEnde": "1400" }

data = { "Produkt": "P101", "Einheit": "kg", "Transport": "Lieferung", "NettoOnlinerabatt": "0", "NettoPreiszuschlagSchlauch": "30", "formURL": "/preise_holzpellets.php", "Mehrwertsteuerfaktor": "1.07", "Mindestmenge": "3000", "NettoEinblaspauschale": "33", "anti_csrf_token": "697c98f324473", "Lieferzeit": "30", "device": "c", "NettoEinzelpreis": "", "NettoEinzelpreisMindestmenge": "", "Bundesland": "BY", "Fahrzeit": "75", "Gebiet": "", "Lager": "", "Lager_id": "", "NettoPreiszuschlagTermin": "", "Gesamtmenge": "", "Lieferfrist": "", "Kundennummer": "", "GesamtPreisManuell": "", "NettoEinblaspauschaleManuell": "33", "KundenBestellnr": "", "Land": "DE", "Notiz": "", "plz": "91086", "menge": "3000", "lieferstellen": "1", "Auftragsnummer": "", "plzLieferanschrift": "91086", "ortLieferanschrift": "Aurachtal" }

data['menge'] = '3000'


data_sack = { "Produkt": "P104", "Einheit": "Pal.", "Transport": "Lieferung", "NettoOnlinerabatt": "0", "formURL": "/preise_pellets_sackware_lieferung.php", "Mehrwertsteuerfaktor": "1.07", "Mindestmenge": "1", "anti_csrf_token": "6989b7abe8cc6", "device": "c", "NettoEinzelpreis": "", "NettoEinzelpreisMindestmenge": "", "Lieferzeit": "30", "Bundesland": "BY", "Palettengewicht": "975", "Fahrzeit": "", "Gebiet": "", "Lager": "", "Lager_id": "", "NettoPreiszuschlagTermin": "", "RZ": "0", "Gesamtmenge": "", "Lieferfrist": "", "Kundennummer": "", "GesamtPreisManuell": "", "KundenBestellnr": "", "Land": "DE", "Notiz": "", "plz": "91086", "menge": "3", "lieferstellen": "1", "Auftragsnummer": "", "plzLieferanschrift": "", "ortLieferanschrift": "", "anrede": "Herr", "vorname": "", "name": "", "firma": "", "firma2": "", "firma3": "", "anschrift": "", "email": "", "telefon1": "", "telefon2": "", "teilmenge": "", "Rabattmarken": "", "Hinweistext": "", "ara": "nein", "RaVorname": "", "RaName": "", "RaFirma": "", "RaFirma2": "", "RaFirma3": "", "RaAnschrift": "", "RaPLZ": "", "RaOrt": "", "RaEmail": "", "RaTelefon1": "", "RaTelefon2": "", "za": "Vorkasse", "Kontoinhaber": "", "iban": "", "bic": "", "bday": "", "bmonth": "", "byear": "", "GebDatum": "", "Zahlungsbetrag": "", "Versandart": "30" }

response      = requests.post(url, data=data)
# print(response.text)
t      = json.loads(response.text)

preis_pro_t = float(t['NettoEinzelpreis'])
menge = float(data['menge'])
pauschale = float(data['NettoEinblaspauschale'])
mwst = float(data['Mehrwertsteuerfaktor'])

gesamtpreis = round( ( menge * preis_pro_t / 1000.0 + pauschale ) * mwst , 2)

date_now = datetime.now().strftime("%d.%m.%Y")

outstring = "{:8s} {:6.0f} {:9.2f} {:15.2f}".format(date_now, menge, preis_pro_t, gesamtpreis)
# print(outstring)


##### Sackware
response_sack = requests.post(url, data=data_sack)
t_sack = json.loads(response_sack.text)
# print(t_sack)
preis_sack = float(t_sack['NettoEinzelpreis'])
menge_sack = float(data_sack['menge'])
gewicht_sack = float(data_sack['Palettengewicht'])
preis_pro_t_sack = ( 1000.0 /gewicht_sack ) * preis_sack
gesamtpreis = round( ( menge_sack * preis_sack ) * mwst , 2)
outstring_sack = "{:6.0f} {:9.2f} {:18.2f}".format(menge_sack, preis_pro_t_sack, gesamtpreis)


print('Datum       Menge   Preis/t     Gesamtpreis   Sack   Preis/t   Gesamtpreis_Sack')
print(outstring, outstring_sack)

with open('pelletspreise', 'a') as file:
  file.write(outstring + ' ' + outstring_sack + '\n')
