class Pair():
    def __init__(self, *points):
        if len(points) != 2:
            raise ValueError
        self.points = frozenset(points)

    def __hash__(self):
        return hash(self.points)

    def __eq__(self, other):
        return isinstance(other, Pair) and self.points == other.points

    # TODO: Look up better way to do *args in repr
    def __repr__(self):
        return f"Pair({', '.join([str(p) for p in self.points])})"
