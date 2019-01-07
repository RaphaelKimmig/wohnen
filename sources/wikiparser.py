from bs4 import BeautifulSoup
import requests


def get_cities(population=True):
    url="https://de.wikipedia.org/wiki/Liste_der_Gro%C3%9F-_und_Mittelst%C3%A4dte_in_Deutschland"
    soup = BeautifulSoup(requests.get(url).content,"html.parser")
    tables = soup.find_all("table",{"class":"wikitable"})
    
    trs=[]
    for table in tables:
        new_trs = table.find_all("tr")
        if len(trs) < len(new_trs):
            trs = new_trs

    cities = {}
    for tr in trs:
        try:
            tds=tr.find_all("td")
            city_name = tds[1].find("a").get("title")
            cities[city_name]={}
            if population:
                cities[city_name]["population"]=int(tds[-2].text.replace(".", ""))
        except:
            pass

    return cities