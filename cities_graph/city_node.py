"""Contains city node definition used to represent each country's city."""

INITIAL_CITY_BALANCE = (
    1_000_000  # At day 1 all cities have this amount of coins of their country's motif
)
DAILY_REPRESENTATIVE_DIVISOR = 1000  # The representative portion divisor for the whole city balance

CountryName = str
CityBalance = dict[CountryName, int]


class CityNode:
    """Makes it easier to encapsulate each city and it's balance."""

    country: str
    balance: CityBalance

    def __init__(self, country: str, country_names: list[str]) -> None:
        """Initialize city node object."""
        self.balance = {country_name: 0 for country_name in country_names}
        self.balance[country] = INITIAL_CITY_BALANCE

        self.country = country

    def __str__(self) -> str:
        """Represents city node as string of it's current balance."""
        return str(self.balance)

    def is_complete(self) -> bool:
        """Checks whether the city is completed."""
        return all(country_motif_amount > 0 for country_motif_amount in self.balance.values())

    def get_representative_portions(self) -> CityBalance:
        """Get representative portion (.001 of each motif) of coins."""
        representative_portions = {}
        for country in self.balance.keys():
            coin_portion = int(self.balance[country] / DAILY_REPRESENTATIVE_DIVISOR)
            representative_portions[country] = coin_portion

        return representative_portions

    def replenish_city_balance(self, portion: CityBalance) -> None:
        """Add coins to city balance."""
        for country_name, replenish_amount in portion.items():
            self.balance[country_name] += replenish_amount

    def withdraw_city_balance(self, portion: CityBalance) -> None:
        """This method is used to withdraw city balance representative portion."""
        for country_name, withdraw_amount in portion.items():
            self.balance[country_name] -= withdraw_amount
