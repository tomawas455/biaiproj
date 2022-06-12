from travelling_salesman_problem.utils import City
from itertools import permutations


class BestWayFinder:
    def __init__(self, cities):
        self.roads = list(permutations(cities))
        self.best_road = None
        self.worst_road = None
        self.average = 0

    def solve(self):
        sum = 0
        dist = Road(self.roads[0]).get_distance()
        self.worst_road = Road(self.roads[0])
        self.best_road = Road(self.roads[0])
        max_dist = dist
        min_dist = dist

        for road in self.roads:
            dist = Road(road).get_distance()
            if max_dist < dist:
                max_dist = dist
                self.worst_road = Road(road)
            if min_dist > dist:
                min_dist = dist
                self.best_road = Road(road)
            sum += dist
        self.average = sum / len(self.roads)
        return


class Road:
    def __init__(self, road):
        self.road = road

    def get_distance(self):
        dist = 0
        for i in range(len(self.road) - 1):
            dist += self.road[i].distance(self.road[i + 1])
        dist += self.road[-1].distance(self.road[0])
        return dist

    def to_str(self):
        result = "["
        for city in self.road:
            result += city.name + "(" + str(city.x) + "," + str(city.y) + "), "
        result += "]"
        return result