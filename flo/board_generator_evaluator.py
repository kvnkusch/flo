import time


class BoardGeneratorEvaluator():
    def __init__(self, board_metric_function=None):
        self._metric_func = board_metric_function

    # TODO: Do some sort of logging of progress here
    def evaluate(self, board_generator, puzzle_size, num_trials):
        trial_results = []
        for i in range(num_trials):
            start = time.time()
            game_state, count = board_generator.generate_board(puzzle_size)
            end = time.time()
            print(f"Trial {i}: {end - start}")

            trial_result = {
                'time': end - start,
                'metric': self._metric_func(game_state)
                if self._metric_func else 0,
                'fail_count': count
            }
            trial_results.append(trial_result)

        return trial_results

    def compare(self, board_generators, puzzle_size, num_trials):
        return [self.evaluate(bg, puzzle_size, num_trials)
                for bg in board_generators]
