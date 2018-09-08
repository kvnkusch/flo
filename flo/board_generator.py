from game_state import GameState
from prob import Distribution
from my_strategy import MyStrategy
from game_plotter import plot_game
from game_board import GridBoard
from game_state import GameState
from collections import Counter
from numpy import random


class BoardGenerator():
    def __init__(self, strategy):
        self.strategy = strategy

    def generate_board(self, size, plot=False, verbose=False):
        unsolvable_count = 0
        game_state = GameState(GridBoard(size, []), [])

        max_pairs = self.strategy.get_max_pairs(game_state)

        while not game_state.is_victory_state():

            extend_path_prob = self.strategy.should_extend_path(game_state,
                                                                max_pairs)
            next_game_state_funcs = []
            probs = []

            if self.strategy.can_extend_path(game_state):
                next_game_state_funcs.append(self.strategy.get_extend_path_game_state)
                probs.append(extend_path_prob)
                # events.append((extend_path_prob, self.strategy.get_extend_path_dist(game_state)))

            if self.strategy.can_add_path(game_state):
                next_game_state_funcs.append(self.strategy.get_new_path_game_state)
                probs.append(1 - extend_path_prob)
                # events.append((1 - extend_path_prob, self.strategy.get_new_path_dist(game_state)))

            if len(next_game_state_funcs) == 1:
                probs[0] = 1

            if not next_game_state_funcs:
                raise ValueError

            next_game_state_func = random.choice(next_game_state_funcs, p=probs)
            game_state = next_game_state_func(game_state)()

            unsolvable_info = self.strategy.get_unsolvable_info(game_state, max_pairs)

            if unsolvable_info.is_unsolvable:
                unsolvable_count += 1
                game_state = self.strategy.resolve_unsolvable_game_state(
                    game_state, unsolvable_info)


        if verbose:
            print("Unsolvable Count: ", unsolvable_count)
        if plot:
            plot_game(game_state)

        return game_state, unsolvable_count


bg = BoardGenerator(MyStrategy())

if __name__ == '__main__':
    bg.generate_board(14, plot=True, verbose=True)
