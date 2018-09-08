class Strategy():
    def __init__(self, max_pairs_decider, should_extend_decider,
                 extend_path_decider, add_path_decider,
                 unsolvable_decider, previous_game_state_decider):
        self._max_pairs_decider = max_pairs_decider
        self._should_extend_decider = should_extend_decider

        self._extend_path_decider = extend_path_decider
        self._add_path_decider = add_path_decider

        self._unsolvable_decider = unsolvable_decider
        self._previous_game_state_decider = previous_game_state_decider

    def get_max_pairs(self, game_state):
        return self._max_pairs_decider.decide(game_state)

    def should_extend_path(self, game_state, max_pairs):
        return self._should_extend_decider.decide(game_state, max_pairs)

    def get_all_extended_path_dist(self, game_state):
        return self._extend_path_decider.decide(game_state)

    def get_all_new_path_dist(self, game_state):
        return self._add_path_decider.decide(game_state)

    def is_unsolvable(self, game_state, max_pairs):
        return self._unsolvable_decider.decide(game_state, max_pairs)

    def get_previous_game_state(self, previous_game_states):
        return self._previous_game_state_decider.decide(previous_game_states)

    def get_clean_game_state(self, game_state):
        return self._clean_game_state_decider.decide(previous_game_states)


class Decider():
    def decide(self):
        raise NotImplementedError


class MaxPairsDecider(Decider):
    """
    Returns int
    """
    def decide(self, game_state):
        pass


class ShouldExtendDecider(Decider):
    """
    Returns float
    """
    def decide(self, game_state, max_pairs):
        pass


class ExtendPathDecider(Decider):
    """
    Returns Distribution<GameState>
    """
    def decide(self, game_state):
        pass


class AddPathDecider(Decider):
    """
    Returns Distribution<GameState>
    """
    def decide(self, game_state):
        pass


class UnsolvableDecider(Decider):
    # TODO: This should return atleast a code and likely trouble points as well
    # Trouble points are only applicable to "bubble" and "unreachable clusters"
    # I think
    """
    Returns boolean
    """
    def decide(self, game_state, max_pairs):
        pass


class PreviousGameStateDecider(Decider):
    """
    Returns ([GameState], GameState)
    """
    def decide(self, previous_game_states):
        pass


class CleanGameStateDecider(Decider):
    """
    Returns GameState
    """
    def decider(self, game_state):
        pass
