from flask import Flask, request, render_template, redirect, url_for
from tic_tac_toe import TicTacToe

#tic_tac_toe = TicTacToe(5)
app2 = Flask(__name__)
object_list = []


@app2.route('/display/<i>')
def display(i):
    ii=int(i)
    x = 1 if object_list[ii].is_relinquishing_starting_turn_possible() else 0
    return render_template('display1.html',
                           positions=object_list[ii].positions,
                           player=object_list[ii].players[0],
                           enable=x,
                           no_of_rows=object_list[ii].no_of_rows,
                           no_of_columns=object_list[ii].no_of_columns,
                           user=ii)


@app2.route("/reset", methods=['POST'])
def reset():
    tic_tac_toe.reset()
    return display()


@app2.route("/switch", methods=['POST'])
def switch():
    if tic_tac_toe.is_relinquishing_starting_turn_possible():
        tic_tac_toe.relinquish_starting_turn()
    else:
        pass
        # flash an error message
    return display()


@app2.route("/<i>")
def index(i):
    return display(i)


@app2.route("/play/<i>", methods=['POST'])
def play(i):
    ii = int(i)
    sub_value = request.form.get('sub')
    sub_value_int = int(sub_value)
    y1 = sub_value_int % 3
    x1 = sub_value_int // 3
    object_list[ii].play(x1, y1)
    winner = object_list[ii].get_winner()
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

    return redirect(url_for("index",i = i))


@app2.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        global tic_tac_toe
        tic_tac_toe = TicTacToe(user)
        object_list.append(TicTacToe(user))
        return None
        #return temp()


@app2.route("/home")
def checking():
    return render_template("home_page.html")


@app2.route("/temp", methods=['POST'])
def GameOptions():
    print(request.method)
    if request.method == 'POST':
        if request.form.get('Enter old room') == 'Enter old room':
            return redirect(url_for("old_room"))
        elif request.form.get('Create new room') == 'Create new room':
            return redirect(url_for("new_room"))


@app2.route("/createnewroom")
def new_room():
    return render_template("newroom.html")


@app2.route("/checkname/<i>")
def temp(i):
    return display(i)


@app2.route('/oldroominput', methods=['POST'])
def oldroominput():
    if request.method == 'POST':
        i = request.form['nm']
        return redirect(url_for('temp', i=i))


@app2.route("/oldroom")
def old_room():
    return render_template("oldroom.html")


app2.run()
