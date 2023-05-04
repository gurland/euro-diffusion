"""Main CLI file to run the algorithm."""
import time
from collections import defaultdict

from cities_graph import CitiesGraph
from utils import get_test_cases, make_case_results_output


def get_country_cities(case_graph: CitiesGraph) -> dict[str, set]:
    """Gets current country cities in a graph."""
    country_cities = defaultdict(lambda: set())
    for city_id, city_node in case_graph:
        country_cities[city_node.country].add(city_id)
    return country_cities


def update_completed_countries(
    completed_countries: set,
    country_cities: dict[str, set],
    completed_cities: set,
    case_results: dict,
    case_number: int,
    current_day: int,
) -> None:
    """Used to check if all cities in a country are completed."""
    for completed_country in completed_countries:
        country_cities.pop(completed_country)
    completed_countries.clear()

    for country_name, city_ids in country_cities.items():
        if completed_cities.intersection(city_ids) == city_ids:
            completed_countries.add(country_name)
            case_results.setdefault(case_number, {})[country_name] = current_day


def process_case(case_number: int, case_text: str, case_results: dict) -> None:
    """Functions simulates a single case until all case cities completed."""
    case_graph = CitiesGraph.from_case_text(case_text)
    if not case_graph:
        return

    country_cities = get_country_cities(case_graph)
    completed_cities = set()
    completed_countries = set()

    current_day = 0
    while country_cities:
        update_completed_countries(
            completed_countries,
            country_cities,
            completed_cities,
            case_results,
            case_number,
            current_day,
        )

        case_graph.simulate_graph_in_a_one_day()
        current_day += 1

        for city_id, city_node in case_graph:
            if city_id in completed_cities:
                continue

            if city_node.is_complete():
                completed_cities.add(city_id)


if __name__ == "__main__":
    input_file_path = input("Enter path to your input file (press enter for default one): ")
    start_time = time.time()

    cases = get_test_cases(input_file_path)

    case_results = {}
    for case_number, case in enumerate(cases):
        process_case(case_number, case, case_results)

    print(make_case_results_output(case_results))
    print(f"Time taken: {time.time() - start_time}s")
