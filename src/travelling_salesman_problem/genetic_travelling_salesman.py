import random

from .utils import (
    TravellingSalesmanError, get_dataset
)


class GeneticTravellingSalesman:
    dataset = None

    def __init__(self, settings):
        if settings is None:
            raise TravellingSalesmanError(
                "I need settings to know what I'm suppossed to do!",
            )
        self.settings = settings

    def solve(self):
        self.dataset = get_dataset(self.settings.filepath)
        generations = [self.create_population()]
        for i, generation in enumerate(range(1, self.settings.generations)):
            # pass n% of best individuals in previous generation to the next
            generations.append(generations[-1][:int(
                self.settings.population
                * self.settings.to_next_generation
            )])
            self.create_population(generations[-2], generations[-1])
        return generations  # [-1][0]

    def create_population(self, previous_population=None, new_population=None):
        population = None
        if previous_population is None:
            dataset_len = len(self.dataset)
            population = [
                Individual(random.sample(self.dataset, dataset_len))
                for _ in range(self.settings.population)
            ]
        else:
            if new_population is None:
                new_population = []
            individuals_to_create = self.settings.population \
                                    - len(new_population)
            parents = previous_population[:int(
                self.settings.population * self.settings.fit_to_crossover
            )]
            for individual in range(individuals_to_create):
                parent1 = random.choice(parents)
                parent2 = parent1
                while parent1 == parent2:
                    parent2 = random.choice(parents)
                new_chromosome = Crossover(
                    parent1.chromosome, parent2.chromosome
                ).cross()
                Mutation(new_chromosome).mutate(
                    self.settings.mutation_probability
                )
                new_population.append(
                    Individual(new_chromosome)
                )
            population = new_population
        population.sort(key=lambda individual: individual.fitness)
        return population


class Individual:
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = self.calculate_fitness()

    def calculate_fitness(self):
        return self.road_length()

    def road_length(self):
        return sum([
            city.distance(self.chromosome[i - 1])
            for i, city in enumerate(self.chromosome)
        ])

    def __repr__(self):
        return 'fitness: ' + str(self.fitness) \
               + ', length: ' + str(self.road_length()) \
               + ' ' + str(self.chromosome)


class Crossover:
    def __init__(self, parent1, parent2):
        self.parent1 = parent1
        self.parent2 = parent2

    def cross(self):
        return random.choice([self.copy_part_and_merge, self.every_other])()

    def copy_part_and_merge(self):
        take_parent, fill_parent = random.sample(
            [self.parent1, self.parent2], 2
        )
        chromosome_len = len(take_parent)
        take_start = random.randrange(0, chromosome_len)
        take_end = random.randrange(take_start + 1, chromosome_len + 1)
        chromosome_range = take_parent[take_start:take_end]
        fill_index = 0
        chromosome = []
        working_chromosome = [c for c in chromosome_range]
        for i in range(chromosome_len):
            if take_start <= i < take_end:
                chromosome.append(take_parent[i])
                working_chromosome.append(take_parent[i])
            else:
                while fill_parent[fill_index] in working_chromosome:
                    fill_index += 1
                chromosome.append(fill_parent[fill_index])
                working_chromosome.append(fill_parent[fill_index])
        return chromosome

    def every_other(self):
        even_parent, odd_parent = random.sample(
            [self.parent1, self.parent2], 2
        )
        chromosome = []
        chromosome_len = len(even_parent)
        even_index = 0
        odd_index = 0
        for i in range(chromosome_len):
            if i % 2:
                while odd_parent[odd_index] in chromosome:
                    odd_index += 1
                chromosome.append(odd_parent[odd_index])
            else:
                while even_parent[even_index] in chromosome:
                    even_index += 1
                chromosome.append(even_parent[even_index])
        return chromosome


class Mutation:
    def __init__(self, chromosome):
        self.chromosome = chromosome

    def mutate(self, probability):
        if random.random() > probability:
            return
        random.choice((
            self.random_swap, self.adjacent_swap,
            self.end_to_end_swap, self.inversion
        ))()

    def random_swap(self):
        first_index = random.randrange(0, len(self.chromosome))
        second_index = first_index
        while second_index == first_index:
            second_index = random.randrange(0, len(self.chromosome))
        self.swap(first_index, second_index)

    def adjacent_swap(self):
        index = random.randrange(0, len(self.chromosome) - 1)
        self.swap(index, index + 1)

    def end_to_end_swap(self):
        lower_max = int(len(self.chromosome) / 2)
        upper_max = round(len(self.chromosome) / 2)
        lower_half = self.chromosome[:lower_max]
        upper_half = self.chromosome[upper_max:]
        self.chromosome[:lower_max] = upper_half
        self.chromosome[upper_max:] = lower_half

    def inversion(self):
        # start is at worst one item before last
        inversion_start = random.randrange(0, len(self.chromosome) - 1)
        # end is at worst element next to start
        inversion_end = random.randrange(
            inversion_start + 1, len(self.chromosome)
        )
        # at worst we do adjacent swap pretending to be inversion
        # now we iterate over half od end - start + 1
        # +1 because end is part of range (it's range inclusive in our case)
        for _ in range(int((inversion_end - inversion_start + 1) / 2)):
            self.swap(inversion_start, inversion_end)
            inversion_start += 1
            inversion_end -= 1

    def swap(self, first_index, second_index):
        self.chromosome[first_index], self.chromosome[second_index] = (
            self.chromosome[second_index], self.chromosome[first_index]
        )
