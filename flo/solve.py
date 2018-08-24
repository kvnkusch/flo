from point import Point
from pair import Pair
from actions import Drag
from game_board import GridBoard
from game_state import GameState
from game_plotter import plot_game


size = 5
pairs = [
    Pair(Point(0, 4), Point(1, 0)),
    Pair(Point(1, 1), Point(2, 4)),
    Pair(Point(2, 0), Point(2, 3)),
    Pair(Point(3, 0), Point(4, 3)),
    Pair(Point(3, 1), Point(4, 4)),
]
board = GridBoard(size, pairs)


actions = [
    # 1st pair
    Drag(Point(1, 0), Point(0, 0)),
    Drag(Point(0, 0), Point(0, 1)),
    Drag(Point(0, 1), Point(0, 2)),
    Drag(Point(0, 2), Point(0, 3)),
    Drag(Point(0, 3), Point(0, 4)),
    # 2nd pair
    Drag(Point(1, 1), Point(1, 2)),
    Drag(Point(1, 2), Point(1, 3)),
    Drag(Point(1, 3), Point(1, 4)),
    Drag(Point(1, 4), Point(2, 4)),
    # 3rd pair
    Drag(Point(2, 0), Point(2, 1)),
    Drag(Point(2, 1), Point(2, 2)),
    Drag(Point(2, 2), Point(2, 3)),
    # 4th pair
    Drag(Point(3, 0), Point(4, 0)),
    Drag(Point(4, 0), Point(4, 1)),
    Drag(Point(4, 1), Point(4, 2)),
    Drag(Point(4, 2), Point(4, 3)),
    # 5th pair
    Drag(Point(3, 1), Point(3, 2)),
    Drag(Point(3, 2), Point(3, 3)),
    Drag(Point(3, 3), Point(3, 4)),
    Drag(Point(3, 4), Point(4, 4)),
]

game_state = GameState(board, [])

for action in actions:
    game_state = game_state.next(action)
    plot_game(game_state)
    if game_state.is_victory_state():
        print("!!! !!! !!! YOU WIN !!! !!! !!!")
