import copy
from typing import Union

CountryName = str
CityBalance = dict[CountryName, int]


class CityNode:
    country: str
    balance: CityBalance

    def __init__(self, country: str, country_names: list[str]):
        self.balance = {country_name: 0 for country_name in country_names}
        self.balance[country] = 1_000_000

        self.country = country

    def __str__(self):
        return str(self.balance)

    def get_representative_portions(self) -> CityBalance:
        representative_portions = {}
        for country in self.balance.keys():
            coin_portion = int(self.balance[country] / 1000)
            representative_portions[country] = coin_portion

        return representative_portions

    def replenish_city_balance(self, portion: CityBalance) -> None:
        for country_name, replenish_amount in portion.items():
            self.balance[country_name] += replenish_amount

    def withdraw_city_balance(self, portion: CityBalance) -> None:
        for country_name, withdraw_amount in portion.items():
            self.balance[country_name] -= withdraw_amount


class CitiesGraphIterator:
    def __init__(self, graph: 'CitiesGraph'):
        root_id, root_node = list(graph.city_nodes.items())[0]

        self.graph = graph
        self.visited = set()
        self.queue = [root_id]

    def __iter__(self):
        return self

    def __next__(self):
        if not self.queue:
            raise StopIteration

        visited_city_id = self.queue.pop()
        self.visited.add(visited_city_id)

        visited_city_node = self.graph.city_nodes[visited_city_id]
        neighbour_city_ids = self.graph.get_adjacent_city_ids(visited_city_id)

        valid_adjacent_city_ids = [
            neighbour_city_id for neighbour_city_id in neighbour_city_ids
            if neighbour_city_id not in self.visited and
               neighbour_city_id not in self.queue
        ]
        self.queue.extend(valid_adjacent_city_ids)

        return visited_city_id, visited_city_node


class CitiesGraph:
    def __init__(self,
                 country_names: list[str] = None,
                 city_nodes: dict[int, CityNode] = None):

        self.country_names = country_names if country_names is not None else []
        self.city_nodes = city_nodes if city_nodes is not None else {}

    def __setitem__(self, coords, city_node):
        x, y = coords
        city_id = 10 * x + y

        if self.city_nodes.get(city_id) is not None:
            raise ValueError("Countries overlap. Error")

        self.city_nodes[city_id] = city_node

    def __getitem__(self, coords):
        x, y = coords
        city_id = 10 * x + y

        return self.city_nodes.get(city_id)

    def __iter__(self):
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
    ):
        for x in range(int(xl), int(xh)+1):
            for y in range(int(yl), int(yh)+1):
                self[x, y] = CityNode(name, self.country_names)

    def get_adjacent_city_ids(self, city_id):
        possible_adjacent_ids = (city_id - 10,  # North
                                 city_id + 10,  # South
                                 city_id - 1,   # West
                                 city_id + 1)   # East

        adjacent_ids = []
        for possible_adjacent_id in possible_adjacent_ids:
            if possible_adjacent_id in self.city_nodes:
                adjacent_ids.append(possible_adjacent_id)

        return adjacent_ids

    def get_graph_in_a_one_day(self):
        next_day_graph = copy.deepcopy(self)

        for city_id, city_node in self:
            daily_representative_portion = city_node.get_representative_portions()
            adjacent_city_ids = self.get_adjacent_city_ids(city_id)

            for adjacent_city_id in adjacent_city_ids:
                next_day_graph.city_nodes[adjacent_city_id].replenish_city_balance(
                    daily_representative_portion
                )

            # Withdraw representative portion of each motif from this city
            # because these were transferred to neighbours
            city_node.withdraw_city_balance({
                country_name: coin_value * len(adjacent_city_ids)
                for country_name, coin_value in daily_representative_portion.items()
            })

            print(city_id, city_node.country)

        return next_day_graph


g = CitiesGraph.from_case_text("""3
France 1 4 4 6
Spain 3 1 6 3
Portugal 1 1 2 2""")


c = g.get_graph_in_a_one_day()

print(c)