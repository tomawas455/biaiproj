import sys
import time

from settings import Settings, SettingsError
from travelling_salesman_problem.permutation_travelling_salesman import PermutationTravellingSalesman
from travelling_salesman_problem.utils import get_dataset, generate_dataset, save_to_file
from travelling_salesman_problem import (
    GeneticTravellingSalesman, TravellingSalesmanError
)

if __name__ == '__main__':
    settings = Settings()
    try:
        settings.get_from_cli_args()

        dataset = settings.generate_dataset_properties

        if dataset is not None:
            generate_dataset(dataset)
        else:
            permutation = None
            permutation_time = None

            start = time.time()
            generations = GeneticTravellingSalesman(settings).solve()
            end = time.time()
            gen_time = end - start
            print(generations[-1][0])
            print("Generation time: " + str(gen_time))

            if settings.find_best_way:
                permutation = PermutationTravellingSalesman(get_dataset(settings.filepath))
                start = time.time()
                permutation.solve()
                end = time.time()
                permutation_time = end - start
                print("\nBest possible length: " + str(permutation.best_road.get_distance()))
                print("Worst possible lenght: " + str(permutation.worst_road.get_distance()))
                print("Generation time: " + str(permutation_time))

            if settings.outputpath is not None:
                save_to_file(generations, gen_time, permutation, permutation_time, settings.outputpath)

    except SettingsError as e:
        print("Could not read options:\n", e.msg, file=sys.__stderr__)
    except TravellingSalesmanError as e:
        print(
            "Could not solve travelling salesman problem:\n",
            e.msg,
            file=sys.__stderr__
        )