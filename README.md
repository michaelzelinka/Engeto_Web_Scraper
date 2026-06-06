# Elections Scraper 2017

Scraper výsledků voleb do Poslanecké sněmovny 2017 z webu volby.cz.

## Instalace

```bash
pip install -r requirements.txt
```

## Spuštění

```bash
python main.py <URL_okresu> <název_výstupního_souboru>
```

## Příklad

```bash
python main.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" "vysledky_benesov.csv"
```

Výstup `vysledky_benesov.csv`:
```
cislo,nazev,volici,obalky,hlasy,Občanská demokratická strana,...
529303,Benešov,13104,8485,8437,1052,...
532568,Bernartice,191,148,148,4,...
```
