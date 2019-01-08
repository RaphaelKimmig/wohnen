from ipyleaflet import *
from ipywidgets import HTML
import ipywidgets as widgets
import numpy as np


def map_values(x, min_in, max_in, min_out, max_out, func="linear"):
    if func == "linear":
        return (x - min_in) * (max_out - min_out) / (max_in - min_in) + min_out
    else:
        return map_values(
            x=x, min_in=min_in, max_in=max_in, min_out=min_out, max_out=max_out
        )


class MapRepresentation:
    m = Map(center=[50.84757295365389, 10.437011718750002], zoom=5)
    minradius = 5
    maxradius = 40
    mapeles = []
    data = []
    dispalydata_size = {}
    dispalydata_color = {}
    cities = {}

    def displaydata(
        self,
        key,
        minimum=-np.inf,
        maximum=np.inf,
        weight=1,
        func="linear",
        effect_color=True,
        effect_size=False,
    ):
        if effect_size:
            self.dispalydata_size[key] = {
                "minimum": minimum,
                "maximum": maximum,
                "weight": weight,
                "func": func,
            }
        if effect_color:
            self.dispalydata_color[key] = {
                "minimum": minimum,
                "maximum": maximum,
                "weight": weight,
                "func": func,
            }

    def update(self):
        for el in self.mapeles:
            if el is not None:
                self.m.remove_layer(el)

        self.mapeles = [None for cm in self.data]

        color_points = [0 for d in self.data]
        size_points = [0 for d in self.data]
        color_weigt_sum = sum(
            [vals["weight"] for key, vals in self.dispalydata_color.items()]
        )
        size_weigt_sum = sum(
            [vals["weight"] for key, vals in self.dispalydata_size.items()]
        )

        for key, attributes in self.dispalydata_size.items():

            maxvalue = min(
                [attributes["maximum"], max([d.get(key) for d in self.data])]
            )
            minvalue = max(
                [attributes["minimum"], min([d.get(key) for d in self.data])]
            )

            for i in range(len(self.data)):
                if key in self.data[i]:
                    if (
                        attributes["minimum"] <= self.data[i][key]
                        and attributes["maximum"] >= self.data[i][key]
                    ):
                        self.mapeles[i] = CircleMarker(weight=1, opacity=0.8)
                        self.mapeles[i].radius = int(
                            map_values(
                                func=attributes["func"],
                                x=self.data[i][key],
                                min_in=minvalue,
                                max_in=maxvalue,
                                min_out=self.minradius,
                                max_out=self.maxradius,
                            )
                        )
                        self.mapeles[i].location = (
                            self.data[i]["lat"],
                            self.data[i]["lon"],
                        )

        for ele in self.mapeles:
            if ele is not None:
                self.m += ele
