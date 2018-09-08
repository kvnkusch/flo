class Strategy():
    def __init__(self, max_pairs_decider, should_extend_decider,
                 extend_path_decider, add_path_decider,
                 resolve_clusters_decider):
        self._max_pairs_decider = max_pairs_decider
        self._should_extend_decider = should_extend_decider

        self._extend_path_decider = extend_path_decider
        self._add_path_decider = add_path_decider

        self._resolve_clusters_decider = resolve_clusters_decider

    def get_max_pairs(self, game_state):
        return self._max_pairs_decider.decide(game_state)

    def should_extend_path(self, game_state, max_pairs):
        return self._should_extend_decider.decide(game_state, max_pairs)

    def get_all_extended_path_dist(self, game_state):
        return self._extend_path_decider.decide(game_state)

    def get_all_new_path_dist(self, game_state):
        return self._add_path_decider.decide(game_state)

    def resolve_clusters(self, game_state, clusters):
        return self._resolve_clusters_decider.decide(game_state, clusters)


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


class ResolveClustersDecider(Decider):
    """
    Returns GameState
    """
    def decider(self, game_state):
        pass
