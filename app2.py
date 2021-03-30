from flask import Flask, request, render_template, redirect, url_for
from tic_tac_toe import TicTacToe


app2 = Flask(__name__)
object_list = {}


@app2.route('/display/<i>')
def display(i):
    x = 1 if object_list[i].is_relinquishing_starting_turn_possible() else 0
    return render_template('display1.html',
                           positions=object_list[i].positions,
                           player=object_list[i].players[0],
                           enable=x,
                           no_of_rows=object_list[i].no_of_rows,
                           no_of_columns=object_list[i].no_of_columns,
                           user=i)


@app2.route("/reset/<i>", methods=['POST'])
def reset(i):
    object_list[i].reset()
    return redirect(url_for("display", i=i))


@app2.route("/switch/<i>", methods=['POST'])
def switch(i):
    if object_list[i].is_relinquishing_starting_turn_possible():
        object_list[i].relinquish_starting_turn()
    else:
        pass
        # flash an error message
    return redirect(url_for("display", i=i))


@app2.route("/<i>")
def index(i):
    return display(i)


@app2.route("/play/<i>", methods=['POST'])
def play(i):
    sub_value = request.form.get('sub')
    sub_value_int = int(sub_value)
    y1 = sub_value_int % 3
    x1 = sub_value_int // 3
    object_list[i].play(x1, y1)
    winner = object_list[i].get_winner()
    if winner is not None:
        return render_template('victory1.html',
                               positions=object_list[i].positions,
                               player=winner,
                               no_of_rows=object_list[i].no_of_rows,
                               no_of_columns=object_list[i].no_of_columns,
                               user=i)

    if object_list[i].is_game_draw():
        return render_template('draw1.html',
                               positions=object_list[i].positions,
                               no_of_rows=object_list[i].no_of_rows,
                               no_of_columns=object_list[i].no_of_columns,
                               user=i)

    return redirect(url_for("index", i=i))


@app2.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        if user in object_list:
            pass # already exists
        else:
            object_list[user] = TicTacToe(user)
        #object_list.append(TicTacToe(user))
        return None



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
        if i in object_list:
            return redirect(url_for('temp', i=i))
        else:
            pass #flash enter valid room


@app2.route("/oldroom")
def old_room():
    return render_template("oldroom.html")


app2.run()
