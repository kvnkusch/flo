from point import Point, PointDelta
import random
from abc import ABCMeta, abstractmethod


class GameBoard(metaclass=ABCMeta):
    def __init__(self, points, pairs):
        self.points = points
        self.pairs = pairs

    def get_adjacent_points(self, path, ignore=None):
        return [[p for p in self.adjacent_points(end_point)
                 if p in self.points and
                 p not in self._get_off_limit_points(ignore) and
                 p not in self._get_folding_points(path, end_point)]
            for end_point in path.end_points()
        ]

    def get_random_point(self, ignore=None):
        non_ignored_points = [p for p in self.points
                              if p not in self._get_off_limit_points(ignore)]
        if non_ignored_points:
            return random.choice(non_ignored_points)

    def get_open_points(self, ignore=None):
        return [p for p in self.points
                if p not in self._get_off_limit_points(ignore)]

    def _get_off_limit_points(self, ignore):
        ignore_points = ignore or []
        pair_points = [p for pair in self.pairs for p in pair.points]
        return pair_points + ignore_points

    def _get_folding_points(self, path, end_point):
        return [adj_pt for pt in path.points
                for adj_pt in self.adjacent_points(pt)
                if pt != end_point]

    def adjacent_points(self, p):
        return [p.with_added_delta(d) for d in self.adjacent_point_deltas]

    @property
    @abstractmethod
    def adjacent_point_deltas(self, p):
        pass

    @abstractmethod
    def without_pairs(self, remove_pairs):
        pass


class GridBoard(GameBoard):
    def __init__(self, size, pairs):
        self.size = size
        points = [Point(x, y) for x in range(size) for y in range(size)]
        super().__init__(points, pairs)

    @property
    def adjacent_point_deltas(self):
        return [
            PointDelta(1, 0),
            PointDelta(0, 1),
            PointDelta(-1, 0),
            PointDelta(0, -1),
        ]

    def without_pairs(self, remove_pairs):
        for pair in remove_pairs:
            if pair not in self.pairs:
                raise ValueError

        keep_pairs = [pr for pr in self.pairs if pr not in remove_pairs]

        return GridBoard(self.size, keep_pairs)
