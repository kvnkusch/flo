class GameState():
    def __init__(self, board, paths):
        self.board = board
        # TODO: Can I make this a tuple???
        self.paths = [p for p in paths if not p.is_empty()]

    def next(self, action):
        return GameState(self.board, action.get_updated_paths(self.board,
                                                              self.paths))

    def is_victory_state(self):
        return self.completed_paths() == len(self.board.pairs) and\
            self.filled_points() == len(self.board.points)

    def completed_paths(self):
        return sum([pr.points == set(pth.end_points())
                    for pr in self.board.pairs
                    for pth in self.paths])

    def filled_points(self):
        return sum([p in pth.points
                    for p in self.board.points
                    for pth in self.paths])

    def get_ignore_points(self):
        return [p for pth in self.paths for p in pth.points]

    def without_paths(self, remove_paths):
        for path in remove_paths:
            if path not in self.paths:
                raise ValueError

        keep_paths = [pth for pth in self.paths if pth not in remove_paths]
        remove_pairs = [pth.get_pair() for pth in remove_paths]

        return GameState(self.board.without_pairs(remove_pairs),
                         keep_paths)
