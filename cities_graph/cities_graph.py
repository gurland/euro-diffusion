from typing import Union
from collections import defaultdict

from .city_node import CityNode
from .cities_graph_iter import CitiesGraphIterator


class CitiesGraph:
    def __init__(self,
                 country_names: list[str] = None,
                 city_nodes: dict[int, CityNode] = None):

        self.country_names = country_names if country_names is not None else []
        self.city_nodes = city_nodes if city_nodes is not None else {}

    def __bool__(self) -> bool:
        return bool(self.city_nodes)

    def __setitem__(self, coords: Union[tuple, int], city_node) -> None:
        if type(coords) == tuple:
            x, y = coords
            city_id = 10 * x + y
        else:
            city_id = coords

        if self.city_nodes.get(city_id) is not None:
            raise ValueError("Countries overlap. Error")

        self.city_nodes[city_id] = city_node

    def __getitem__(self, coords: Union[tuple, int]) -> CityNode:
        if type(coords) == tuple:
            x, y = coords
            city_id = 10 * x + y
        else:
            city_id = coords

        return self.city_nodes.get(city_id)

    def __iter__(self) -> CitiesGraphIterator:
        return CitiesGraphIterator(self)

    @classmethod
    def from_case_text(cls, case_text: str) -> 'CitiesGraph':
        case_lines = case_text.splitlines()
        country_count = int(case_lines[0].strip())

        country_cities = {}

        for country_index in range(1, country_count+1):
            country_name, *country_coords = case_lines[country_index].strip().split(" ")
            country_cities[country_name] = country_coords

        new_graph = cls(
            country_names=list(country_cities.keys())
        )

        for country_name, country_coords in country_cities.items():
            new_graph.add_country_cities(country_name, *country_coords)

        return new_graph

    def add_country_cities(
            self,
            name: str,
            xl: Union[str, int], yl: Union[str, int],  # Left bottom corner
            xh: Union[str, int], yh: Union[str, int]   # Right top corner
    ) -> None:
        for x in range(int(xl), int(xh)+1):
            for y in range(int(yl), int(yh)+1):
                self[x, y] = CityNode(name, self.country_names)

    def get_adjacent_city_ids(self, city_id: int) -> list[int]:
        possible_adjacent_ids = (city_id - 10,  # North
                                 city_id + 10,  # South
                                 city_id - 1,   # West
                                 city_id + 1)   # East

        adjacent_ids = []
        for possible_adjacent_id in possible_adjacent_ids:
            if possible_adjacent_id in self.city_nodes:
                adjacent_ids.append(possible_adjacent_id)

        return adjacent_ids

    def simulate_graph_in_a_one_day(self) -> None:
        city_replenish_portions = defaultdict(lambda: [])  # city_id: list[portions]
        withdraw_portions = {}  # city_id: portion

        for city_id, city_node in self:
            daily_representative_portion = city_node.get_representative_portions()
            adjacent_city_ids = self.get_adjacent_city_ids(city_id)

            for adjacent_city_id in adjacent_city_ids:
                city_replenish_portions[adjacent_city_id].append(daily_representative_portion)

            withdraw_portions[city_id] = {
                country_name: coin_value * len(adjacent_city_ids)
                for country_name, coin_value in daily_representative_portion.items()
            }

        for city_id, replenish_portions in city_replenish_portions.items():
            for replenish_portion in replenish_portions:
                self.city_nodes[city_id].replenish_city_balance(replenish_portion)

        for city_id, withdraw_portion in withdraw_portions.items():
            self.city_nodes[city_id].withdraw_city_balance(withdraw_portion)
