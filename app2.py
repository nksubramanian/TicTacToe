from flask import Flask, request, redirect, url_for, render_template


class TicTacToe:

    def __init__(self):
        self.positions = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.players = ['x', 'o']
        self.no_of_rows = 3
        self.no_of_columns = 3

    def reset(self):
        self.positions = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.players = ['x', 'o']

    def relinquish_starting_turn(self):
        if self.is_relinquishing_starting_turn_possible():
            self.players.reverse()
        else:
            raise Exception("Unsupported Operation relinquishing")

    def is_relinquishing_starting_turn_possible(self):
        for row in self.positions:
            for element in row:
                if element != 0:
                    return False
        return True

    def play(self, x, y):
        self.positions[x][y] = self.players[0]
        self.players.reverse()
        #have to validate if cell is already played

    def who_won_with_pattern(self, pattern):
        x1, y1 = pattern[0]
        val = self.positions[x1][y1]
        if val == 0:
            return None
        for (x, y) in pattern:
            if val != self.positions[x][y]:
                return None
        return val

    def get_winner(self):
        winning_patterns = [[(0, 0), (1, 1), (2, 2)],
                            [(0, 0), (0, 1), (0, 2)],
                            [(1, 0), (1, 1), (1, 2)],
                            [(2, 0), (2, 1), (2, 2)],
                            [(0, 0), (1, 0), (2, 0)],
                            [(0, 1), (1, 1), (2, 1)],
                            [(0, 2), (1, 2), (2, 2)],
                            [(0, 2), (1, 1), (2, 0)]]

        for pattern in winning_patterns:
            winner = self.who_won_with_pattern(pattern)
            if winner is not None:
                return winner
        return None

    def is_game_draw(self):
        for rows in self.positions:
            for element in rows:
                if element == 0:
                    return False
        return True


tic_tac_toe = TicTacToe()
app2 = Flask(__name__)


@app2.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)

    if request.method == 'POST':
        sub_value = request.form.get('sub')
        if sub_value == "Reset":
            tic_tac_toe.reset()
            return redirect(url_for("fff"))
        if sub_value == "Switch":
            if tic_tac_toe.is_relinquishing_starting_turn_possible():
                tic_tac_toe.relinquish_starting_turn()
            else:
                pass
                #flash an error message
            return redirect(url_for("fff"))

        sub_value_int = int(sub_value)
        y1 = sub_value_int % 3
        x1 = sub_value_int // 3
        tic_tac_toe.play(x1, y1)
        winner = tic_tac_toe.get_winner()
        if winner is not None:
            return render_template('victory1.html',
                                   positions=tic_tac_toe.positions,
                                   player=winner,
                                   no_of_rows=tic_tac_toe.no_of_rows,
                                   no_of_columns=tic_tac_toe.no_of_columns)

        if tic_tac_toe.is_game_draw():
            return render_template('draw1.html',
                                   positions=tic_tac_toe.positions,
                                   no_of_rows=tic_tac_toe.no_of_rows,
                                   no_of_columns=tic_tac_toe.no_of_columns)

    return redirect(url_for("fff"))


@app2.route("/fff")
def fff():
    x = 1 if tic_tac_toe.is_relinquishing_starting_turn_possible() else 0
    return render_template('display1.html',
                           positions=tic_tac_toe.positions,
                           player=tic_tac_toe.players[0],
                           enable=x,
                           no_of_rows=tic_tac_toe.no_of_rows,
                           no_of_columns=tic_tac_toe.no_of_columns)






















app2.run()
