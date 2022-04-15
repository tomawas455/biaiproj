import json
import math
from textwrap import dedent


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
