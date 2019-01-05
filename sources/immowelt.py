import urllib, json
def get_immowelt_data(startdate="2018-01-01",enddate="2019-01-01"):
    urlst="https://www.immowelt.de/immobilienpreise/proxy?"\
    "geoid=108"\
    "&estatetype=H%C3%A4user"\
    "&distributiontype=Kauf"\
    "&dimensiontype=geobeschreibung"\
    "&facttype=quadratmeterpreiskauf"\
    "&date="+startdate+":"+enddate
    data = urllib.request.urlopen(urlst).read()
    data_json = data[data.index(b"{"):data.rindex(b"}")+1]
    data=json.loads(data_json)
    
    cities={
        data["xAxis"]["categories"][i]:(data["series"][0]["data"][i]["y"],data["series"][1]["data"][i]["low"],data["series"][1]["data"][i]["high"])
        for i in range(len(data["xAxis"]["categories"]))
    }
    return cities