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
            next_game_states = []
            probs = []

            extend_path_game_state = self.strategy.get_extend_path_game_state(game_state)
            new_path_game_state = self.strategy.get_new_path_game_state(game_state)

            if extend_path_game_state is not None:
                next_game_states.append(extend_path_game_state)
                probs.append(extend_path_prob)

            if new_path_game_state is not None:
                next_game_states.append(new_path_game_state)
                probs.append(1 - extend_path_prob)

            if len(next_game_states) == 1:
                probs[0] = 1

            if not next_game_states:
                raise ValueError

            game_state = random.choice(next_game_states, p=probs)()

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
    bg.generate_board(12, plot=True, verbose=True)
