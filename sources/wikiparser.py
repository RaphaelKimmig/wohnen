from bs4 import BeautifulSoup
import requests
import json
from ipywidgets import IntProgress
from IPython.display import display

api_props = {"coordinates": "coordinates", "alias": "pageterms"}
api_prop_answer = {"pageterms": "terms"}


def get_cities(
    wikiurl=True, population=True, coordinates=True, alias=True, start=0, end=100000
):

    BASE_URL = "https://de.wikipedia.org"
    url = BASE_URL + "/wiki/Liste_der_Gro%C3%9F-_und_Mittelst%C3%A4dte_in_Deutschland"

    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    tables = soup.find_all("table", {"class": "wikitable"})

    trs = []
    for table in tables:
        new_trs = table.find_all("tr")
        if len(trs) < len(new_trs):
            trs = new_trs

    cities = {}
    api_params = []
    if coordinates:
        api_params.append(api_props["coordinates"])
    if alias:
        api_params.append(api_props["alias"])

    f = IntProgress(min=0, max=len(trs[start:end]) - 1)  # instantiate the bar
    display(f)

    for tr in trs[start:end]:
        try:
            f.value += 1
            tds = tr.find_all("td")
            city_name = tds[1].find("a").get("title")
            data = {}
            wikiname = tds[1].find("a").get("href").rsplit("/", 1)[-1]
            if wikiurl:
                data["wikiurl"] = BASE_URL + tds[1].find("a").get("href")
            if population:
                data["population"] = int(tds[-2].text.replace(".", ""))
            if len(api_params) > 0:
                citydata = wiki_api(title=wikiname, props=api_params)
                data = {**data, **citydata}
            data["names"] = data.get("names", []) + [wikiname]
            cities[city_name] = data

        except:
            pass

    return cities


def wiki_api(title, props, lang="de"):
    propstring = "|".join(props)
    url = (
        "https://"
        + lang
        + ".wikipedia.org/w/api.php?action=query&format=json&prop="
        + propstring
        + "&titles="
        + title
    )
    props = [api_prop_answer.get(prop, prop) for prop in props]

    data_items = [
        (key, val)
        for key, val in json.loads(requests.get(url).text)["query"]["pages"].items()
    ]
    # data = {titles[i]:{prop : data_items[i][1][prop] for prop in props if prop in data_items[i][1]} for i in range(len(data_items))}
    data = {prop: val for prop, val in data_items[0][1].items() if prop in props}

    if api_props["coordinates"] in props:
        try:
            data["lon"] = data[api_props["coordinates"]][0]["lon"]
            data["lat"] = data[api_props["coordinates"]][0]["lat"]
            del data[api_props["coordinates"]]
        except:
            pass

    if api_prop_answer.get(api_props["alias"], api_props["alias"]) in props:
        try:
            prop = api_prop_answer.get(api_props["alias"], api_props["alias"])
            data["names"] = data[prop].get("alias", []) + data[prop].get("label", [])
            del data[prop]
        except:
            pass

    return data
