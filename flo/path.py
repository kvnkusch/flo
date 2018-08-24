from pair import Pair


class Path():
    def __init__(self, points):
        self.points = points

    def shorten(self, point, include=True):
        short_points = self.points[:self.points.index(point) +
                                   (1 if include else 0)]
        return Path(short_points)

    def extend(self, point):
        return Path(self.points + [point])

    def flip(self):
        return Path(self.points[::-1])

    def chop(self, point):
        if len(self.points[self.points.index(point) + 1:]) >\
                len(self.points[:self.points.index(point)]):
            return self.flip().shorten(point, include=False)
        else:
            return self.shorten(point, include=False)

    def end_points(self):
        return self.points[0], self.points[-1]

    def continuation_points(self):
        if self.is_empty():
            return None, None
        beg_delta = self.points[0].get_delta_from(self.points[1])
        end_delta = self.points[-1].get_delta_from(self.points[-2])
        return (self.points[0].with_added_delta(beg_delta),
                self.points[-1].with_added_delta(end_delta))

    def get_pair(self):
        return Pair(*self.end_points())

    def is_empty(self):
        return len(self.points) == 1

    def __eq__(self, other):
        return isinstance(other, Path) and\
            self.points == other.points

    def __repr__(self):
        return f"Path({self.points})"
