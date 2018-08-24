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
game_state = GameState(board, [])

while not game_state.is_victory_state():
    inp = input("Move: ")
    if inp == "show":
        plot_game(game_state)
    else:
        x1, y1, x2, y2 = [int(inp[i]) for i in range(4)]
        action = Drag(Point(x1, y1), Point(x2, y2))
        game_state = game_state.next(action)

print("!!! !!! !!! YOU WIN !!! !!! !!!")
