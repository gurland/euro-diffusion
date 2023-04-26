from cities_graph import CityNode, CitiesGraph


if __name__ == '__main__':
    g = CitiesGraph.from_case_text("""3
    France 1 4 4 6
    Spain 3 1 6 3
    Portugal 1 1 2 2""")

    country_cities = {}
    for city_id, city_node in g:
        country_cities.setdefault(city_node.country, set()).add(city_id)

    print(country_cities)

    completed_cities = set()
    completed_countries = set()

    for i in range(10000):
        for completed_country in completed_countries:
            country_cities.pop(completed_country)
        completed_countries.clear()

        for city_id, city_node in g:
            if city_id in completed_cities:
                continue

            if city_node.is_complete():
                completed_cities.add(city_id)

        for country_name, city_ids in country_cities.items():
            if completed_cities == {11, 12, 21, 22}:
                print("qwe")
            if completed_cities.intersection(city_ids) == city_ids:
                completed_countries.add(country_name)
                print(f"Completed country {country_name} in {i} days")
        g = g.get_graph_in_a_one_day()
