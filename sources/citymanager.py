import warnings,csv,json

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
    
class City():
    def __init__(self,name,names=[],**kwargs):
        self.attr = kwargs
        self.attr["names"] = list(set(names) - {name})
        self.name = name
        

    def has_name(self,name):
        if self.attr["main_name"] == name:
            return True
        for n in self.attr["names"]:
            if n == name:
                return True
        return False
    
    def add_name(self,name):
        if isinstance(name,list):
            return [self.add_name(c) for c in city]
        
        if not isinstance(name,str):
            warnings.warn(str(name)+" is not a string (city name)")
            return 
        
        if name != self.name:
            self.attr["names"] = list(set(self.attr["names"] + [name]))
            
    def set_attributes(self,**kwargs):
        self.attr = {**self.attr,**kwargs}
    
    def get_main_name(self):
        return self.attr.get("main_name")
    
    def set_main_name(self,name):
        list(set(self.attr["names"] + [self.name])-{name})
        self.attr["main_name"]=name
        
    name = property(get_main_name, set_main_name)
    
class CityDataManager():
    def __init__(self,csv=None):
        self.cities = {}
        
        if csv is not None:
            self.load_from_csv(csv)
    
    def load_from_csv(self,csvfile,clear=True):
        try:
            new_cities={}
            with open(csvfile, 'r+') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    for k,e in row.items():
                        if len(e)>0:
                            row[k] =json.loads(e)
                        else:
                            row[k] = None
                    new_cities[row["main_name"]]=City(name =row["main_name"], **row)
                    
            if clear:
                self.cities = new_cities
            else:
                self.cities = {**self.cities, **new_cities}
        except FileNotFoundError:
            warnings.warn("File not found")
    
    def save_to_csv(self,csvfile):
        keys=set()
        for city_name, city in self.cities.items():
            keys = keys | set(city.attr.keys())
            
        with open(csvfile, "w+") as f:
            writer = csv.DictWriter(f,keys)
            writer.writeheader()
            for city_name, city in self.cities.items():
                writer.writerow(
                {k: json.dumps(to_number(e)) for k,e in city.attr.items()}
                )
                
    def get_city_by_name(self,name):
        if name in self.cities:
            return self.cities[name]
    
        for city_name,city in self.cities.items():
            if city.has_name(name):
                return city
        
        return None
    
    
    def add_city(self,cityname):
        if isinstance(cityname,list):
            return [self.add_city(c) for c in city]
        
        if not isinstance(cityname,str):
            warnings.warn(str(cityname)+" is not a string (cityname)")
            return None
        
        city = self.get_city_by_name(cityname)
        if city is not None:
            return city
        
        try:
            city = self.cities[cityname] = City(name=cityname)
        except Exception as e:
            print(e)
            warnings.warn("Problems adding city: "+str(cityname))
            return None
                              
        return city
        
    def add_attributes(self,name,city_dict):
        return self.add_city_dict({city:{name:value} for city,value in city_dict.items()})
    
    def add_city_dict(self,city_dict):
        for city_name,properties in city_dict.items():
            city = self.get_city_by_name(city_name)
            if city is None:
                city = self.add_city(city_name)
            if city is not None:
                city.set_attributes(**properties)
    