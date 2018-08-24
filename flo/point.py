from flyweight import MetaFlyweight


class Point(metaclass=MetaFlyweight):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def get_delta_from(self, other):
        return PointDelta(self.x - other.x, self.y - other.y)

    def with_added_delta(self, delta):
        return Point(self.x + delta.x, self.y + delta.y)


class PointDelta(metaclass=MetaFlyweight):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"PointDelta({self.x}, {self.y})"
