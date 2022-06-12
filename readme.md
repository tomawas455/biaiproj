# BIAI project

## Travelling salesman problem

### help:
Usage: python src/main.py \[options\] \<dataset\><br/>
&emsp;-h --help -> Shows help<br/>
&emsp;-g --generations -> Set amount of generations to create, 10 by default<br/>
&emsp;-p --population -> Set each generation population size, 20 by default<br/>
&emsp;-n --nextgen -> Set amount of individuals that go into next generation, 0.1 by default<br/>
&emsp;-c --crossover -> Set amount of individuals that can crossover to create new generation<br/>
&emsp;-m --mutation -> Set probability of mutation of individual, 0.02 by default<br/>
&emsp;-o --output -> Save output to file<br/>
&emsp;-d --generate-dataset -> Generate new dataset file<br/>
&emsp;-f --find-best-way -> Compare genetic algorithm with best possible way<br/>
<br/>
dataset format:<br/>
&emsp;JSON file that's array of objects.<br/>
&emsp;each point/city needs name and x/y coords.<br/>
&emsp;eg. [<br/>
&emsp;&emsp;{"name":"A", "x":1, "y":1},<br/>
&emsp;&emsp;{"name":"B", "x":2, "y":2}<br/>
&emsp;]
