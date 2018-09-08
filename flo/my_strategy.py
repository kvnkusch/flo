from strategy import Strategy, UnsolvableInfo
from game_board import GridBoard
from game_state import GameState
from prob import Distribution
from path import Path
from pair import Pair

import random


class MyStrategy():

    def get_max_pairs(self, game_state):
        return game_state.board.size

    def should_extend_path(self, game_state, max_pairs):
        num_pairs = len(game_state.board.pairs)
        if num_pairs == 0:
            return 0
        elif num_pairs < max_pairs:
            return (num_pairs / max_pairs) ** .25
        else:
            return 1

    def can_extend_path(self, game_state):
        path_dists = []
        for path in game_state.paths:
            extend_path_dist = self._get_path_extended_path_dist(
                path, game_state)
            if extend_path_dist.not_empty():
                return True
        return False

    def can_add_path(self, game_state):
        ignore = game_state.get_ignore_points()
        for seed_point in game_state.board.get_open_points(ignore=ignore):
            add_path_dist = self._get_path_extended_path_dist(
                Path([seed_point]), game_state)
            if add_path_dist.not_empty():
                return True
        return False

    def get_extend_path_game_state(self, game_state):
        path_dists = []
        for path in game_state.paths:
            path_dists.append(self._get_path_extended_path_dist(
                path, game_state))
        return Distribution.uniform(path_dists).choice()

    def get_new_path_game_state(self, game_state):
        seed_point_dists = []
        ignore = game_state.get_ignore_points()
        for seed_point in game_state.board.get_open_points(ignore=ignore):
            seed_point_dists.append(
                self._get_path_extended_path_dist(Path([seed_point]),
                                                  game_state))
        return Distribution.uniform(seed_point_dists).choice()

    # TODO: What's going on here???
    # It works but I forgot why
    def get_unsolvable_info(self, game_state, max_pairs):
        eligible_points = self._get_eligible_points(game_state)
        open_clusters = self._get_open_point_clusters(game_state)

        isolated_clusters = [
            cluster for cluster in open_clusters
            if not cluster & eligible_points
        ]

        unreachable_clusters = [
            cluster for cluster in isolated_clusters
            if len(cluster) < 3 or len(game_state.paths) == max_pairs
        ]

        return UnsolvableInfo(
            len(unreachable_clusters) > 0,
            {
                'unreachable_clusters': unreachable_clusters
            }
        )

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

    def resolve_unsolvable_game_state(self, game_state, unsolvable_info):
        bad_paths = []
        for cluster in unsolvable_info.data['unreachable_clusters']:
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

    def _get_path_extended_path_dist(self, path, game_state):
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

            next_game_state_func = self._get_extended_path_game_state_funcs(
                 adj_point, adj_point in beg_adj_pts, path, game_state)
            adj_point_dists.append((relative_prob, next_game_state_func))

        return Distribution(adj_point_dists)

    def _get_extended_path_game_state_funcs(self,
                                            adj_point,
                                            adj_to_beg,
                                            to_extend_path,
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
