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
        if is_game_won():
            return render_template('victory.html', positions=positions, player=who_won())
        if is_game_draw():
            return render_template('draw.html', positions=positions)

    x.reverse()

    return redirect(url_for("fff"))


@app2.route("/fff")
def fff():
    return render_template('display.html', positions=positions, player=x[0])


def is_game_draw():
    for i in range(0, 3):
        for j in range(0, 3):
            if positions[i][j] == 0:
                return False
    return True


def is_game_won():
    if positions[0][0] == positions[1][1] == positions[2][2] != 0:
        return True
    elif positions[0][0] == positions[0][1] == positions[0][2] != 0:
        return True
    elif positions[1][0] == positions[1][1] == positions[1][2] != 0:
        return True
    elif positions[2][0] == positions[2][1] == positions[2][2] != 0:
        return True
    elif positions[0][0] == positions[1][0] == positions[2][0] != 0:
        return True
    elif positions[0][1] == positions[1][1] == positions[2][1] != 0:
        return True
    elif positions[0][2] == positions[1][2] == positions[2][2] != 0:
        return True
    elif positions[0][2] == positions[1][1] == positions[2][0] != 0:
        return True
    else:
        return False


def who_won():
    if positions[0][0] == positions[1][1] == positions[2][2] != 0:
        return positions[0][0]
    elif positions[0][0] == positions[0][1] == positions[0][2] != 0:
        return positions[0][0]
    elif positions[1][0] == positions[1][1] == positions[1][2] != 0:
        return positions[1][0]
    elif positions[2][0] == positions[2][1] == positions[2][2] != 0:
        return positions[2][0]
    elif positions[0][0] == positions[1][0] == positions[2][0] != 0:
        return positions[0][0]
    elif positions[0][1] == positions[1][1] == positions[2][1] != 0:
        return positions[0][1]
    elif positions[0][2] == positions[1][2] == positions[2][2] != 0:
        return positions[0][1]
    elif positions[0][2] == positions[1][1] == positions[2][0] != 0:
        return positions[0][2]


app2.run()
