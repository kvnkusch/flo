def my_metric_function(game_state):
    score = 0

    number_of_corners = 0
    for path in game_state.paths:
        last_pt = None
        last_pt_delta = None
        for pt in path.points:
            if last_pt is None:
                last_pt = pt
            elif last_pt_delta is None:
                last_pt_delta = pt - last_pt
                last_pt = pt
            else:
                new_pt_delta = pt - last_pt
                if new_pt_delta != last_pt_delta:
                    number_of_corners += 1
                    last_pt_delta = new_pt_delta
                last_pt = pt

    longest_path = max([len(path.points) for path in game_state.paths])

    score += number_of_corners + longest_path

    return score
