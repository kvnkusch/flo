import matplotlib.pyplot as plt


RADIUS = 0.4

COLORS = [
    'b', 'g', 'r', 'y', 'c', 'm', 'k',
    'aqua', 'maroon', 'fuchsia', 'lime',
    'silver', 'gray', 'olive', 'navy',
    'teal',
]


def plot_game(game_state):
    fig, ax = plt.subplots()
    color_count = 0
    pair_color_map = {}

    # Eventually figure this out programatically
    linewidth = 160 / game_state.board.size

    for pair in game_state.board.pairs:
        for point in pair.points:
            ax.add_artist(plt.Circle((point.x + 0.5, point.y + 0.5),
                                     RADIUS, color=COLORS[color_count]))
        pair_color_map[pair] = COLORS[color_count]
        color_count += 1

    for pth in game_state.paths:
        pair = [p for p in game_state.board.pairs
                if set(pth.points) & p.points][0]
        ax.plot([p.x + 0.5 for p in pth.points],
                [p.y + 0.5 for p in pth.points],
                color=pair_color_map[pair],
                linewidth=linewidth, linestyle='-')

    ax.set_xlim(0, game_state.board.size)
    ax.set_ylim(0, game_state.board.size)

    ax.grid(color='k', linestyle='-', linewidth=1)

    plt.show()
