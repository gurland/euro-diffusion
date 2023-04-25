from typing import Union


class CitiesGraph:
    def __init__(self):
        self.nodes = {}

    def add_country(
            self,
            name: str,
            xl: Union[str, int], yl: Union[str, int],  # Left bottom corner
            xh: Union[str, int], yh: Union[str, int]   # Right top corner
    ):
        for x in range(int(xl), int(xh)):
            for y in range(int(yl), int(yh)):
                self.nodes[x+y] = name


def parse_initial_graph(country_count, text):
    g = CitiesGraph()
    for country_line in text.splitlines():
        g.add_country(*country_line.strip().split(" "))

    return g


g = parse_initial_graph(1, """France 1 4 4 6
Spain 3 1 6 3
Portugal 1 1 2 2""")


