import csv


def get_citites():
    with open("../data/destatis-staedte.csv", "r") as f:
        reader = csv.DictReader(f)
        cities = {
            entry['Stadt']: int(entry['Bevölkerung insgesamt'].replace(" ", ""))
            for entry in reader
        }
    return cities
