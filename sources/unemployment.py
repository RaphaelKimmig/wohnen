from openpyxl import load_workbook
import requests
import io


def get_unemployment_numbers(
    url="https://statistik.arbeitsagentur.de/Statistikdaten/Detail/201712/iiia6/bzg-bzg-quali/bzg-quali-dlkrdaa-0-201712-xlsx.xlsx"
):
    response = requests.get(url)
    workbook = load_workbook(io.BytesIO(response.content))
    sheet = workbook["Kreise"]
    rows = list(sheet.rows)
    assert rows[9][1].value == "01001 Flensburg, Stadt"

    cities = {}
    for row in rows[9:]:
        if not row[1].value:
            break
        maybe_id, name = row[1].value.split(" ", 1)
        cities[name] = {
            "kreis_id?": maybe_id,
            "insgesamt": row[3].value,
            "Ohne abgeschlossene Berufsausbildung": row[4].value,
            "Betriebliche/ schulische Ausbildung": row[5].value,
            "Akademische Ausbildung": row[6].value,
        }
    return cities


# Bezugsgrößen für Qualifikationsgruppen nach Regionen - Dezember 2017
# https://statistik.arbeitsagentur.de/Statistikdaten/Detail/201712/iiia6/bzg-bzg-quali/bzg-quali-dlkrdaa-0-201712-xlsx.xlsx
