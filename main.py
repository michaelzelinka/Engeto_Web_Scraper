import re
import csv
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def nacti_stranku(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.ok:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        return None

def ziskej_obce(obsah):
    cisla = obsah.find_all('td', {'class': 'cislo'})
    nazvy = obsah.find_all('td', {'class': 'overflow_name'})
    obce = []
    for cislo, nazev in zip(cisla, nazvy):
        obce.append({
            'cislo': cislo.get_text(),
            'nazev': nazev.get_text(),
            'url': urljoin('https://volby.cz/pls/ps2017nss/', cislo.find('a')['href'])
        })
    return obce


def ziskej_vysledky_obce(url):
    obsah = nacti_stranku(url)
    volici = obsah.find('td', {'headers': 'sa2'}).get_text().replace('\xa0', '')
    obalky = obsah.find('td', {'headers': 'sa3'}).get_text().replace('\xa0', '')
    hlasy = obsah.find('td', {'headers': 'sa6'}).get_text().replace('\xa0', '')

    nazvy_stran = obsah.find_all('td', {'class': 'overflow_name'})
    hlasy_stran = obsah.find_all('td', {'headers': re.compile('t1sb3|t2sb3')})

    strany = {}
    for nazev, hlasy_strany in zip(nazvy_stran, hlasy_stran):
        strany[nazev.get_text()] = hlasy_strany.get_text().replace('\xa0', '')

    return {'volici': volici, 'obalky': obalky, 'hlasy': hlasy, **strany}

def uloz_do_csv(data, jmeno_souboru):
    fieldnames = list(data[0].keys())
    with open(jmeno_souboru, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def main():
    if len(sys.argv) != 3:
        print("Zadej URL a název souboru")
        sys.exit()

    url = sys.argv[1]
    jmeno_souboru = sys.argv[2]

    obsah = nacti_stranku(url)
    if not obsah:
        print("Nedostupná stránka")
        sys.exit()

    obce = ziskej_obce(obsah)
    data = []
    for obec in obce:
        vysledky = ziskej_vysledky_obce(obec['url'])
        radek = {
            'cislo': obec['cislo'],
            'nazev': obec['nazev'],
            **vysledky
        }
        data.append(radek)

    uloz_do_csv(data, jmeno_souboru)

main()
