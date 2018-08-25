# from point import Point
from game_board import GridBoard
from game_state import GameState
from game_plotter import plot_game
from path import Path
from pair import Pair
from prob import Distribution

import random


def generate_grid_board(size):
    unsolvable_count = 0
    previous_game_states = []
    game_state = GameState(GridBoard(size, []), [])
    while not game_state.is_victory_state():
        previous_game_states.append(game_state)

        extend_path_prob = should_extend_path_prob(len(game_state.board.pairs),
                                                   size)
        next_game_state_dist = Distribution([
            (extend_path_prob, get_all_extended_path_dist(game_state)),
            (1 - extend_path_prob, get_all_new_path_dist(game_state)),
        ])

        next_game_state_func = next_game_state_dist.choice()
        game_state = next_game_state_func()

        if is_unsolvable(game_state):
            unsolvable_count += 1
            # This jump back could be greatly improved but I don't know how
            previous_game_states, game_state = get_previous_game_state(
                previous_game_states)

    print("Unsolvable Count: ", unsolvable_count)
    plot_game(game_state)
    return game_state.board


def can_extent_path():
    return True


def can_add_new_path():
    pass


def get_previous_game_state(previous_game_states):
    """
    Returns a tuple of previous_game_states and game_state,
    derived from chopping up the passed in previous_game_states
    """

    i = random.randrange(len(previous_game_states))
    print("Length of Game States", len(previous_game_states))
    print("Chosen index", i)
    return previous_game_states[:i], previous_game_states[i]


def should_extend_path_prob(num_pairs, size):
    """
    Returns float in (0, 1)

    Return value is probablity that an existing path should be extended,
    given the number of pairs on the board and the size of the board.

    Exponent value pushes values down in favor of extending a path
    """
    max_num_pairs = get_max_num_pairs(size)
    if num_pairs == 0:
        return 0
    elif num_pairs < max_num_pairs:
        return (num_pairs / max_num_pairs) ** .25
    else:
        return 1


def get_max_num_pairs(size):
    return size


def get_all_extended_path_dist(game_state):
    path_dists = []
    for path in game_state.paths:
        path_dists.append(get_path_extended_path_dist(
            path, game_state))
    return Distribution.uniform(path_dists)


def get_path_extended_path_dist(path, game_state):
    adj_point_dists = []
    ignore_pts = get_ignore_points(game_state)

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
                      [get_pair(pth) for pth in new_paths]),
            new_paths
        )
    return get_extended_path_game_state


def get_all_new_path_dist(game_state):
    seed_point_dists = []
    ignore = get_ignore_points(game_state)
    for seed_point in game_state.board.get_open_points(ignore=ignore):
        seed_point_dists.append(
            get_path_extended_path_dist(Path([seed_point]), game_state))
    return Distribution.uniform(seed_point_dists)


def get_pair(path):
    return Pair(*path.end_points())


def get_ignore_points(game_state):
    return [p for pth in game_state.paths for p in pth.points]


# TODO: Could probably be a lot better
def is_unsolvable(game_state):
    if game_state.is_victory_state():
        return False

    # First, find all adjacent points for all path end points
    eligible_pts = get_eligible_points(game_state)
    if not eligible_pts:
        return True

    # Then, find open_pt_clusters
    open_pt_clusters = get_open_point_clusters(game_state)

    # Check for "bubbles" aka clusters of size one
    #   (one or two eventually if I outlaw paths of length two)
    # If a bubble has no intersection with eligible points, return True
    for cluster in open_pt_clusters:
        if len(cluster) == 1:
            if not cluster & eligible_pts:
                return True

    # Only check the other clusters if I can't add any more pairs
    if len(game_state.board.pairs) < get_max_num_pairs(game_state.board.size):
        return False

    # If every open_pt_cluster intersects with eligible_pts, return False
    # Otherwise that cluster cannot be reached and the puzzle is unsolvable
    # Thus return True
    for cluster in open_pt_clusters:
        if not cluster & eligible_pts:
            return True

    return False


def get_open_point_clusters(game_state):
    ignore_pts = get_ignore_points(game_state)
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


def get_eligible_points(game_state):
    ignore_pts = get_ignore_points(game_state)
    return set([
        pt
        for pth in game_state.paths
        for end_pt_adjacent_pts in game_state.board.get_adjacent_points(
            pth, ignore=ignore_pts)
        for pt in end_pt_adjacent_pts
    ])


if __name__ == '__main__':
    board = generate_grid_board(8)
    plot_game(GameState(board, []))
