import sys

from settings import Settings, SettingsError
from travelling_salesman_problem import (
    GeneticTravellingSalesman, TravellingSalesmanError
)

if __name__ == '__main__':
    settings = Settings()
    try:
        settings.get_from_cli_args()
        best_individual = GeneticTravellingSalesman(settings).solve()
        print(best_individual)
    except SettingsError as e:
        print("Could not read options:\n", e.msg, file=sys.__stderr__)
    except TravellingSalesmanError as e:
        print(
            "Could not solve travelling salesman problem:\n",
            e.msg,
            file=sys.__stderr__
        )
