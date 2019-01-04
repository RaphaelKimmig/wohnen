import csv

# data from https://www.destatis.de/DE/ZahlenFakten/LaenderRegionen/Regionales/Gemeindeverzeichnis/Administrativ/Aktuell/05Staedte.xlsx?__blob=publicationFile

def get_citites():
    with open("../data/destatis-staedte.csv", "r") as f:
        reader = csv.DictReader(f)
        cities = {
            entry['Stadt']: int(entry['Bevölkerung insgesamt'].replace(" ", ""))
            for entry in reader
        }
    return cities
