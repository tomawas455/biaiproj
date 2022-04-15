# BIAI project

## Travelling salesman problem

### help:
Usage: python src/main.py \[options\] \<dataset\><br/>
    -h --help -> Shows help<br/>
    -g --generations -> Set amount of generations to create, 10 by default<br/>
    -p --population -> Set each generation population size, 20 by default<br/>
    -n --nextgen -> Set amount of individuals that go into next generation, 0.1 by default<br/>
    -c --crossover -> Set amount of individuals that can crossover to create new generation<br/>
    -m --mutation -> Set probability of mutation of individual, 0.02 by default<br/>
    -o --output -> Save output to file<br/>
<br/>
dataset format:<br/>
    JSON file that's array of objects.<br/>
    each point/city needs name and x/y coords.<br/>
    eg. [<br/>
        {"name":"A", "x":1, "y":1},<br/>
        {"name":"B", "x":2, "y":2}<br/>
    ]
