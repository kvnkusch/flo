from point import Point, PointDelta
import random
from abc import ABCMeta, abstractmethod


class GameBoard(metaclass=ABCMeta):
    def __init__(self, points, pairs, adjacent_point_deltas):
        self.points = points
        self.pairs = pairs
        self.adjacent_point_deltas = adjacent_point_deltas
        self._adjacent_points_cache = {}

    def get_adjacent_points(self, path, ignore_points):
        return [[p for p in self.adjacent_points(end_point)
                 if p in self.points and
                 p not in self._get_folding_points(path, end_point) and
                 p not in self._get_off_limit_points(ignore_points)]
            for end_point in path.end_points()
        ]

    def get_open_points(self, ignore_points):
        return [p for p in self.points
                if p not in self._get_off_limit_points(ignore_points)]

    def _get_off_limit_points(self, ignore_points):
        pair_points = [p for pair in self.pairs for p in pair.points]
        return pair_points + ignore_points

    def _get_folding_points(self, path, end_point):
        return [adj_pt for pt in path.points
                for adj_pt in self.adjacent_points(pt)
                if pt != end_point]

    def adjacent_points(self, point):
        if point in self._adjacent_points_cache:
            return self._adjacent_points_cache[point]
        else:
            adj_points = [point + d for d in self.adjacent_point_deltas]
            self._adjacent_points_cache[point] = adj_points
            return adj_points

    @abstractmethod
    def without_pairs(self, remove_pairs):
        pass


class GridBoard(GameBoard):
    def __init__(self, size, pairs):
        self.size = size
        points = [Point(x, y) for x in range(size) for y in range(size)]
        adjacent_point_deltas = [
            PointDelta(1, 0),
            PointDelta(0, 1),
            PointDelta(-1, 0),
            PointDelta(0, -1),
        ]
        super().__init__(points, pairs, adjacent_point_deltas)

    def without_pairs(self, remove_pairs):
        for pair in remove_pairs:
            if pair not in self.pairs:
                raise ValueError

        # Changing this to be mutative to persist the cache
        # self.pairs = [pr for pr in self.pairs if pr not in remove_pairs]
        # return self

        keep_pairs = [pr for pr in self.pairs if pr not in remove_pairs]
        return GridBoard(self.size, keep_pairs)
