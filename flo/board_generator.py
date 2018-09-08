from game_state import GameState
from prob import Distribution
from my_strategy import my_strategy1
from game_plotter import plot_game
from game_board import GridBoard
from game_state import GameState
from collections import Counter


class BoardGenerator():
    def __init__(self, strategy):
        self.strategy = strategy

    # TODO: This should return a namedtuple result
    def generate_board(self, size, plot=False, verbose=False):
        unsolvable_count = 0
        game_state = GameState(GridBoard(size, []), [])

        max_pairs = self.strategy.get_max_pairs(game_state)

        while not game_state.is_victory_state():

            extend_path_prob = self.strategy.should_extend_path(game_state,
                                                                max_pairs)

            next_game_state_dist = Distribution([
                (extend_path_prob, self.strategy.get_all_extended_path_dist(game_state)),
                (1 - extend_path_prob, self.strategy.get_all_new_path_dist(game_state)),
            ])

            next_game_state_func = next_game_state_dist.choice()
            game_state = next_game_state_func()

            isolated_clusters = self.get_isolated_clusters(game_state)
            unreachable_clusters = [
                cluster for cluster in isolated_clusters
                if len(cluster) < 3 or len(game_state.paths) == max_pairs
            ]

            if unreachable_clusters:
                unsolvable_count += 1
                game_state = self.strategy.resolve_clusters(
                    game_state, unreachable_clusters)

        if verbose:
            print("Unsolvable Count: ", unsolvable_count)
        if plot:
            plot_game(game_state)
        return game_state.board, unsolvable_count

    def get_isolated_clusters(self, game_state):
        eligible_points = self._get_eligible_points(game_state)
        open_clusters = self._get_open_point_clusters(game_state)

        return [
            cluster for cluster in open_clusters
            if not cluster & eligible_points
        ]

    @staticmethod
    def _get_eligible_points(game_state):
        ignore_pts = game_state.get_ignore_points()
        return set([
            pt
            for pth in game_state.paths
            for end_pt_adjacent_pts in game_state.board.get_adjacent_points(
                pth, ignore=ignore_pts)
            for pt in end_pt_adjacent_pts
        ])

    # TODO: This looks weird at first glance but works for now
    @staticmethod
    def _get_open_point_clusters(game_state):
        ignore_pts = game_state.get_ignore_points()
        open_pt_clusters = []
        open_pts = game_state.board.get_open_points(ignore=ignore_pts)
        visited_pts = set()

        for pt in open_pts:
            if pt not in visited_pts:
                current_cluster = set([pt])
                queue = [pt]

                while queue:
                    current_pt = queue.pop()
                    neighbors = game_state.board.adjacent_points(current_pt)
                    for n in neighbors:
                        if n in open_pts and n not in visited_pts:
                            visited_pts.add(n)
                            current_cluster.add(n)
                            queue.append(n)

                open_pt_clusters.append(current_cluster)

        return open_pt_clusters


new_bg  = NewBoardGenerator(my_strategy1)

if __name__ == '__main__':
    # new_bg.generate_board(8, plot=True, verbose=True)
    new_bg.generate_board(12)
