from flask import Flask, request, redirect, url_for, render_template


app2 = Flask(__name__)
positions = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
players = ['x', 'o']


@app2.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    player = players[0]
    if request.method == 'POST':
        sub_value = request.form.get('sub')
        if sub_value == "Reset":
            reset()
            return redirect(url_for("fff"))
        if sub_value == "Switch":
            players.reverse()
            return redirect(url_for("fff"))

        sub_value_int = int(sub_value)
        y1 = sub_value_int % 3
        x1 = sub_value_int // 3
        positions[x1][y1] = player
        players.reverse()
        winner = who_won()
        if winner is not None:
            return render_template('victory.html', positions=positions, player=winner)
        if is_game_draw():
            return render_template('draw.html', positions=positions)

    return redirect(url_for("fff"))


@app2.route("/fff")
def fff():
    return render_template('display.html', positions=positions, player=players[0], enable=switch_conditions())


def is_game_draw():
    for rows in positions:
        for element in rows:
            if element == 0:
                return False
    return True


def who_won_with_pattern(pattern):
    x1, y1 = pattern[0]
    val = positions[x1][y1]
    if val == 0:
        return None
    for (x, y) in pattern:
        if val != positions[x][y]:
            return None
    return val


def who_won():
    winning_patterns = [[(0, 0), (1, 1), (2, 2)],
                        [(0, 0), (0, 1), (0, 2)],
                        [(1, 0), (1, 1), (1, 2)],
                        [(2, 0), (2, 1), (2, 2)],
                        [(0, 0), (1, 0), (2, 0)],
                        [(0, 1), (1, 1), (2, 1)],
                        [(0, 2), (1, 2), (2, 2)],
                        [(0, 2), (1, 1), (2, 0)]]

    for pattern in winning_patterns:
        winner = who_won_with_pattern(pattern)
        if winner is not None:
            return winner
    return None


def reset():
    global positions
    positions = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    global players
    players = ['x', 'o']
    return redirect(url_for("fff"))


def switch_conditions():
    for row in positions:
        for element in row:
            if element != 0:
                return 0
    return 1


@app2.route("/ddd")
def lighter():
    return render_template("checking", positions=[[0, 0, 0], [0, 0, 0], [0, 0, 0]])




app2.run()


