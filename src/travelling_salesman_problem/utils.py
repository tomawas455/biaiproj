import json
import math
import os.path
from textwrap import dedent
import string
import random

class TravellingSalesmanError(Exception):
    def __init__(self, msg):
        self.msg = msg


class City:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

    def distance(self, other):
        return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def __repr__(self):
        return self.name + '(' + str(self.x) + ', ' + str(self.y) + ')'

    def is_equal_coordinates(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False


def get_dataset(filepath):
    with open(filepath, 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise TravellingSalesmanError(
                'Could not read dataset:\n' + e.msg
            )
        else:
            cities = []
            for city in data:
                name = city.get('name')
                x, y = city.get('x'), city.get('y')
                if name is None or x is None or y is None:
                    raise TravellingSalesmanError(
                        dedent('''\
                            Dataset is missing city\'s name,\
                            x coord or y coord (fields "name", "x", "y")\
                        ''')
                    )
                cities.append(City(name, x, y))
            return cities


def name_of_point(n):
    if n < 0:
        return ''
    result = ''
    if int(n / 26) > 0:
        result += name_of_point(int(n / 26 - 1))
    result += string.ascii_uppercase[n % 26]
    return result


def generate_dataset(dataset_properties):
    min_x = dataset_properties.min_x
    max_x = dataset_properties.max_x
    min_y = dataset_properties.min_y
    max_y = dataset_properties.max_y
    file_name = dataset_properties.file_name
    amount = dataset_properties.amount

    if min_x > max_x or min_y > max_y:
        print("Error, check min/max value of x and y")
        return
    if (max_x - min_x + 1) * (max_y - min_y + 1) < amount:
        print("Count of point is more than possible.")
        return
    cities = []
    for i in range(amount):
        city = City(name_of_point(i),
                    random.choice(list(range(min_x, max_x))),
                    random.choice(list(range(min_y, max_y))))
        repeat = True
        while repeat:
            repeat = False
            for c in cities:
                if city.is_equal_coordinates(c):
                    repeat = True
                    break
            if repeat:
                city.x += 1
                if city.x > max_x:
                    city.x = min_x
                    city.y += 1
                    if city.y > max_y:
                        city.y = min_y
        cities.append(city)
    result = json.dumps([city.__dict__ for city in cities])

    temp = 0
    while os.path.exists(file_name):
        if temp == 0:
            file_name = file_name.rstrip('.json')
        else:
            file_name = file_name.rstrip(str(temp-1) + '.json')
        file_name += str(temp) + '.json'
        temp += 1

    with open(file_name, 'w') as f:
        f.write(str(result))
        f.close()

    return result


def save_to_file(genetic, genetic_time, finder, finder_time, file_name="result.txt"):
    temp = 0
    show_f = True
    if finder is None or finder_time is None:
        show_f = False
    while os.path.exists(file_name):
        if temp == 0:
            file_name = file_name.rstrip('.txt')
        else:
            file_name = file_name.rstrip(str(temp-1) + '.txt')
        file_name += str(temp) + '.txt'
        temp += 1
    with open(file_name, 'w') as f:
        if show_f:
            f.write("Best possible length: " + str(finder.best_road.get_distance()) + "\n")
            f.write("Worst possible length: " + str(finder.worst_road.get_distance()) + "\n")
            f.write("Average length: " + str(finder.average) + "\n")
            f.write("Brute force time: " + str(finder_time) + "\n")
            f.write("Best possible way: " + finder.best_road.to_str() + "\n")
            f.write("Genetic " + str(finder_time/genetic_time) + " times faster\n")
            f.write("Genetic " + str(genetic[-1][0].road_length()/finder.best_road.get_distance() * 100)
                    + "% of best possible length\n\n\n")
        f.write("Genetic algorithm length: " + str(genetic[-1][0].road_length()) + "\n")
        f.write("Genetic algorithm time: " + str(genetic_time) + "\n")
        f.write("Genetic algorithm road: " + str(genetic[-1][0].chromosome) + "\n")
        for i in range(len(genetic)):
            f.write(str(i) + ": " + str(genetic[i][0]) + "\n")

        f.close()