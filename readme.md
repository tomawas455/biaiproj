# BIAI project

## Travelling salesman problem

### help:
Usage: python main.py \[options\] \<dataset\>
-h --help -> Shows help
-g --generations -> Set amount of generations to create, 10 by default
-p --population -> Set each generation population size, 20 by default
-n --nextgen -> Set amount of individuals that go into next generation, 0.1 by default
-c --crossover -> Set amount of individuals that can crossover to create new generation
-m --mutation -> Set probability of mutation of individual, 0.02 by default
-o --output -> Save output to file

dataset format:
    JSON file that's array of objects.
    each point/city needs name and x/y coords.
    eg. [
        {"name":"A", "x":1, "y":1},
        {"name":"B", "x":2, "y":2}
    ]
