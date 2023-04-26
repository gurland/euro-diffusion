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

    def is_complete(self) -> bool:
        return all(
            [country_motif_amount > 0 for country_motif_amount in self.balance.values()]
        )

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
