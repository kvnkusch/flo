from flyweight import MetaFlyweight


class Point(metaclass=MetaFlyweight):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._add_delta_cache = {}

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def __sub__(self, other):
        return PointDelta(self.x - other.x, self.y - other.y)

    def __add__(self, delta):
        if delta in self._add_delta_cache:
            return self._add_delta_cache[delta]
        else:
            value = Point(self.x + delta.x, self.y + delta.y)
            self._add_delta_cache[delta] = value
            return value


class PointDelta(metaclass=MetaFlyweight):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"PointDelta({self.x}, {self.y})"
