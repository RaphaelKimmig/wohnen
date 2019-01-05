import csv
import json
import copy
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent='myapplication')
cities={}
unwanted_fetch_geo_data = ['osm_type','type','display_name', 'licence', 'icon', 'importance', 'class']

def load_cities():
    with open("data/city_data.csv", "r+") as f:
            reader = csv.DictReader(f)
            for row in reader:
                for k,e in row.items():
                    if len(e)>0:
                        row[k] =json.loads(e)
                cities[row["names"][0]]=dict(row)

def to_number(ele):
    if isinstance(ele, int) or isinstance(ele, float):
        return ele
    if type(ele)==list:
        return [to_number(e) for e in ele]
    if ele.isdigit():
        return int(ele)
    try:
        return float(ele)
    except:
        return ele
    
    
def save_cities():
#    keys=set(list([(c.keys()) for n,c in cities.items()]))
    keys=set()
    for n,c in cities.items():
        keys = keys | set(c.keys())
    with open("data/city_data.csv", "w+") as f:
        writer = csv.DictWriter(f,keys)
        writer.writeheader()
        for n,c in cities.items():
            c2 = copy.deepcopy(c)
            for k,e in c2.items():
                e = to_number(e)
                c2[k] = json.dumps(e)
            writer.writerow(c2)
        

def get_base_name(city_name):
    if city_name in cities:
        return city_name
    
    for name,city in cities.items():
        for n in city.get("names",[]):
            if n == city_name:
                return name
    return None


def fetch_geo_data(city_name):
    try:
        location = geolocator.geocode(city_name + ", Germany")
    except Exception as e:
        print("\x1b[31m\""+str(e)+"\"\x1b[0m")
        location = None
        
    if location is None:
        return (None,None)
    name=location.raw["display_name"]
    for todel in unwanted_fetch_geo_data:
        try:
            del location.raw[todel]
        except:
            pass
    cities[name]={**location.raw,**cities.get(name,{})}
    cities[name]["names"]=[name]+list(set([city_name]+cities[name].get("names",[]))-{name})
    return (name,cities[name])

def add_city(city_name,save=True):
    bn = get_base_name(city_name)
    if bn is None:
        n,c = fetch_geo_data(city_name)
    else:
        n,c = bn,cities[bn]
        
    if n is None:
        return (None,None)
    
    if save:
        save_cities()
    return (n,c)

load_cities()