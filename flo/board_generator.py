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

    def generate_grid_board(self, size):
        unsolvable_counter = Counter()
        game_state = GameState(GridBoard(size, []), [])
        previous_game_states = []

        max_pairs = self.strategy.get_max_pairs(game_state)

        while not game_state.is_victory_state():
            previous_game_states.append(game_state)

            extend_path_prob = self.strategy.should_extend_path(game_state,
                                                                max_pairs)

            next_game_state_dist = Distribution([
                (extend_path_prob, self.strategy.get_all_extended_path_dist(game_state)),
                (1 - extend_path_prob, self.strategy.get_all_new_path_dist(game_state)),
            ])

            next_game_state_func = next_game_state_dist.choice()
            game_state = next_game_state_func()

            # Return value of 0 means puzzle is solvable
            unsolvable_code = self.strategy.is_unsolvable(game_state, max_pairs)
            if unsolvable_code:
                unsolvable_counter[unsolvable_code] += 1

                # if unsolvable_code == 1:
                # This jump back could likely be improved
                previous_game_states, game_state = self.strategy\
                    .get_previous_game_state(previous_game_states)
                # elif unsolvable_code in (2, 3):


        print("Unsolvable Details: ", unsolvable_counter)
        plot_game(game_state)
        return game_state.board


BoardGenerator(my_strategy1).generate_grid_board(8)
