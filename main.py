from cities_graph import CitiesGraph
from utils import get_test_cases, make_case_results_output
import time


if __name__ == '__main__':
    input_file_path = input("Enter path to your input file (press enter for default one): ")
    start_time = time.time()

    cases = get_test_cases(input_file_path)

    case_results: dict[int, dict[list, int]] = {}

    for case_number, case in enumerate(cases):
        case_graph = CitiesGraph.from_case_text(case)
        if not case_graph:
            break

        country_cities = defaultdict(lambda: set())
        for city_id, city_node in case_graph:
            country_cities[city_node.country].add(city_id)

        completed_cities = set()
        completed_countries = set()

        current_day = 0
        while country_cities:
            for completed_country in completed_countries:
                country_cities.pop(completed_country)
            completed_countries.clear()

            for city_id, city_node in case_graph:
                if city_id in completed_cities:
                    continue

                if city_node.is_complete():
                    completed_cities.add(city_id)

            for country_name, city_ids in country_cities.items():
                if completed_cities.intersection(city_ids) == city_ids:
                    completed_countries.add(country_name)
                    case_results.setdefault(case_number, {})[country_name] = current_day

            current_day += 1

            case_graph = case_graph.get_graph_in_a_one_day()

    print(make_case_results_output(case_results))
    print(f"Time taken: {time.time() - start_time}s")
