from strategy import (
    Strategy, MaxPairsDecider, ShouldExtendDecider,
    ExtendPathDecider, AddPathDecider, ResolveClustersDecider
)
from game_board import GridBoard
from game_state import GameState
from prob import Distribution
from path import Path
from pair import Pair

import random


# TODO: Judge [-2 ... 2]
class MyMaxPairsDecider(MaxPairsDecider):
    def decide(self, game_state):
        return game_state.board.size


class MyShouldExtendDecider(ShouldExtendDecider):
    def decide(self, game_state, max_pairs):
        num_pairs = len(game_state.board.pairs)
        if num_pairs == 0:
            return 0
        elif num_pairs < max_pairs:
            return (num_pairs / max_pairs) ** .25
        else:
            return 1


# def get_all_extended_path_dist(game_state):
#     path_dists = []
#     for path in game_state.paths:
#         path_dists.append(get_path_extended_path_dist(
#             path, game_state))
#     return Distribution.uniform(path_dists)


def get_path_extended_path_dist(path, game_state):
    adj_point_dists = []
    ignore_pts = game_state.get_ignore_points()

    beg_adj_pts, end_adj_pts = game_state.board.get_adjacent_points(
        path, ignore=ignore_pts + path.points)

    # Continuation points is a heuristic to get better puzzles
    continuation_pts = path.continuation_points()
    any_continuation_pts = any(pt in continuation_pts
                               for pt in beg_adj_pts + end_adj_pts)

    for adj_point in beg_adj_pts + end_adj_pts:
        # # Old method that only had increased probability
        # relative_prob = 1 if adj_point not in continuation_pts else\
        #     len(beg_adj_pts) if adj_point in beg_adj_pts else\
        #     len(end_adj_pts)

        if any_continuation_pts:
            relative_prob = 1 if adj_point in continuation_pts else 0
        else:
            relative_prob = 1

        next_game_state_func = get_extended_path_game_state_funcs(
             adj_point, adj_point in beg_adj_pts, path, game_state)
        adj_point_dists.append((relative_prob, next_game_state_func))

    return Distribution(adj_point_dists)


def get_extended_path_game_state_funcs(adj_point, adj_to_beg, to_extend_path,
                                       game_state):
    # This is the latest way to avoid doing excess pre-computation but
    # it is still beating around the bush.
    def get_extended_path_game_state():
        new_paths = [p for p in game_state.paths if p != to_extend_path]
        new_paths += [Path([adj_point] + to_extend_path.points)
                      if adj_to_beg else
                      Path(to_extend_path.points + [adj_point])]

        return GameState(
            GridBoard(game_state.board.size,
                      [pth.get_pair() for pth in new_paths]),
            new_paths
        )
    return get_extended_path_game_state


# def get_all_new_path_dist(game_state):
#     seed_point_dists = []
#     ignore = game_state.get_ignore_points()
#     for seed_point in game_state.board.get_open_points(ignore=ignore):
#         seed_point_dists.append(
#             get_path_extended_path_dist(Path([seed_point]), game_state))
#     return Distribution.uniform(seed_point_dists)


class MyExtendPathDecider(ExtendPathDecider):
    def decide(self, game_state):
        path_dists = []
        for path in game_state.paths:
            path_dists.append(get_path_extended_path_dist(
                path, game_state))
        return Distribution.uniform(path_dists)


class MyAddPathDecider(AddPathDecider):
    def decide(self, game_state):
        seed_point_dists = []
        ignore = game_state.get_ignore_points()
        for seed_point in game_state.board.get_open_points(ignore=ignore):
            seed_point_dists.append(
                get_path_extended_path_dist(Path([seed_point]), game_state))
        return Distribution.uniform(seed_point_dists)


class MyResolveClustersDecider(ResolveClustersDecider):
    def decide(self, game_state, clusters):
        bad_paths = []
        for cluster in clusters:
            for path in game_state.paths:
                # TODO: There is some unnecessary computation here
                # Could do a pre-loop over paths and hash the "path_adj_points"
                # result
                path_adj_points = set([
                    point
                    for path_pt in path.points
                    for point in game_state.board.adjacent_points(path_pt)
                ])
                if cluster & path_adj_points:
                    bad_paths.append(path)
                    # This limits to removing one path per cluster, which seems
                    # reasonable to me (instead of removing all of them)
                    break

        return game_state.without_paths(bad_paths)


my_strategy1 = Strategy(
    MyMaxPairsDecider(),
    MyShouldExtendDecider(),
    MyExtendPathDecider(),
    MyAddPathDecider(),
    MyResolveClustersDecider(),
)
