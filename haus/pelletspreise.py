#!/usr/bin/python

import requests, json
from datetime import datetime

url = "https://1heiz-pellets.de/x_preis.php"

# data_full = { "Produkt": "P101", "Einheit": "kg", "Transport": "Lieferung", "NettoOnlinerabatt": "0", "NettoPreiszuschlagSchlauch": "30", "formURL": "/preise_holzpellets.php", "Mehrwertsteuerfaktor": "1.07", "Mindestmenge": "3000", "NettoEinblaspauschale": "33", "anti_csrf_token": "697c98f324473", "Lieferzeit": "30", "device": "c", "NettoEinzelpreis": "", "NettoEinzelpreisMindestmenge": "", "Bundesland": "BY", "Fahrzeit": "75", "Gebiet": "", "Lager": "", "Lager_id": "", "NettoPreiszuschlagTermin": "", "Gesamtmenge": "", "Lieferfrist": "", "Kundennummer": "", "GesamtPreisManuell": "", "NettoEinblaspauschaleManuell": "33", "KundenBestellnr": "", "Land": "DE", "Notiz": "", "plz": "91086", "menge": "3000", "lieferstellen": "1", "Auftragsnummer": "", "plzLieferanschrift": "91086", "ortLieferanschrift": "Aurachtal", "anrede": "Herr", "vorname": "", "name": "", "firma": "", "firma2": "", "firma3": "", "anschrift": "", "email": "", "telefon1": "", "telefon2": "", "teilmenge": "", "Rabattmarken": "", "schlauch": "30", "Hinweistext": "", "ara": "nein", "RaVorname": "", "RaName": "", "RaFirma": "", "RaFirma2": "", "RaFirma3": "", "RaAnschrift": "", "RaPLZ": "", "RaOrt": "", "RaEmail": "", "RaTelefon1": "", "RaTelefon2": "", "za": "Vorkasse", "Kontoinhaber": "", "iban": "", "bic": "", "bday": "", "bmonth": "", "byear": "", "GebDatum": "", "Zahlungsbetrag": "", "MontagStart": "0800", "MontagEnde": "1400", "DienstagStart": "0800", "DienstagEnde": "1400", "MittwochStart": "0800", "MittwochEnde": "1400", "DonnerstagStart": "0800", "DonnerstagEnde": "1400", "FreitagStart": "0800", "FreitagEnde": "1400" }

data = { "Produkt": "P101", "Einheit": "kg", "Transport": "Lieferung", "NettoOnlinerabatt": "0", "NettoPreiszuschlagSchlauch": "30", "formURL": "/preise_holzpellets.php", "Mehrwertsteuerfaktor": "1.07", "Mindestmenge": "3000", "NettoEinblaspauschale": "33", "anti_csrf_token": "697c98f324473", "Lieferzeit": "30", "device": "c", "NettoEinzelpreis": "", "NettoEinzelpreisMindestmenge": "", "Bundesland": "BY", "Fahrzeit": "75", "Gebiet": "", "Lager": "", "Lager_id": "", "NettoPreiszuschlagTermin": "", "Gesamtmenge": "", "Lieferfrist": "", "Kundennummer": "", "GesamtPreisManuell": "", "NettoEinblaspauschaleManuell": "33", "KundenBestellnr": "", "Land": "DE", "Notiz": "", "plz": "91086", "menge": "3000", "lieferstellen": "1", "Auftragsnummer": "", "plzLieferanschrift": "91086", "ortLieferanschrift": "Aurachtal" }

data['menge'] = '3000'

response = requests.post(url, data=data)
# print(response.text)
t = json.loads(response.text)
preis_pro_t = float(t['NettoEinzelpreis'])

menge = float(data['menge'])
pauschale = float(data['NettoEinblaspauschale'])
mwst = float(data['Mehrwertsteuerfaktor'])

gesamtpreis = round( ( menge * preis_pro_t / 1000.0 + pauschale ) * mwst , 2)

date_now = datetime.now().strftime("%d.%m.%Y")

print('Datum       Menge   Preis/t     Gesamtpreis')
print("{:8s} {:6.0f} {:9.2f} {:15.2f}".format(date_now, menge, preis_pro_t, gesamtpreis))
