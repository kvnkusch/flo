from abc import ABCMeta, abstractmethod
from collections import namedtuple


UnsolvableInfo = namedtuple('UnsolvableInfo', ['is_unsolvable', 'data'])


class Strategy(metaclass=ABCMeta):

    @abstractmethod
    def get_max_pairs(self, game_state):
        """
        Returns int
        """

    @abstractmethod
    def should_extend_path(self, game_state, max_pairs):
        """
        Returns float
        """

    @abstractmethod
    def get_extend_path_game_state(self, game_state):
        """
        Returns Optional<GameState>
        """

    @abstractmethod
    def get_new_path_game_state(self, game_state):
        """
        Returns Optional<GameState>
        """

    @abstractmethod
    def get_unsolvable_info(self, game_state, max_pairs):
        """
        Returns UnsolvableInfo
        """

    @abstractmethod
    def resolve_unsolvable_game_state(self, game_state, unsolvable_info):
        """
        Returns GameState
        """
