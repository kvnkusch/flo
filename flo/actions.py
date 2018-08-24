from abc import ABCMeta, abstractmethod
from path import Path


class Action(metaclass=ABCMeta):
    @abstractmethod
    def get_updated_paths(self, board, paths):
        pass


class Click(Action):
    def __init__(self, point):
        self.point = point

    def get_updated_paths(self, board, paths):
        return [p.shorten(self.point)
                if self.point in p.points else p
                for p in paths]


class Drag(Action):
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_updated_paths(self, board, paths):
        if self.start in [p for pth in paths for p in pth.points]:
            return [p.shorten(self.start).extend(self.end)
                    if self.start in p.points else
                    p.chop(self.end)
                    if self.end in p.points else
                    p for p in paths]
        elif self.start in [p for pr in board.pairs for p in pr.points]:
            return [p.chop(self.end)
                    if self.end in p.points else
                    p for p in paths] + [Path([self.start, self.end])]
        else:
            return paths

    def __repr__(self):
        return f"Drag({self.start}, {self.end})"
