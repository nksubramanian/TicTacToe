from flask import Flask, request, redirect, url_for, render_template


app2 = Flask(__name__)
positions = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

x = ['x', 'o']


@app2.route("/", methods=['GET', 'POST'])
def index():
    print(request.method)
    y = x[0]
    if request.method == 'POST':
        if request.form.get('sub') == '00':
            positions[0][0] = y
        if request.form.get('sub') == '01':
            positions[0][1] = y
        if request.form.get('sub') == '02':
            positions[0][2] = y
        if request.form.get('sub') == '10':
            positions[1][0] = y
        if request.form.get('sub') == '11':
            positions[1][1] = y
        if request.form.get('sub') == '12':
            positions[1][2] = y
        if request.form.get('sub') == '20':
            positions[2][0] = y
        if request.form.get('sub') == '21':
            positions[2][1] = y
        if request.form.get('sub') == '22':
            positions[2][2] = y

        x.reverse()

        winner = who_won()
        if winner is not None:
            return render_template('victory.html', positions=positions, player=winner)
        if is_game_draw():
            return render_template('draw.html', positions=positions)

    return redirect(url_for("fff"))


@app2.route("/fff")
def fff():
    return render_template('display.html', positions=positions, player=x[0])


def is_game_draw():
    for i in positions:
        for j in i:
            if j == 0:
                return False
    return True


def who_won_with_pattern(pattern):
    x1, y1 = pattern[0]
    val = positions[x1][y1]
    if val == 0:
        return None
    for (x2, y2) in pattern:
        if val != positions[x2][y2]:
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


app2.run()

