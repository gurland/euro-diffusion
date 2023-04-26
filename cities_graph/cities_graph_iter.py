from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .cities_graph import CitiesGraph


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
