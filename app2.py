from flask import Flask, request, render_template, redirect, url_for
from tic_tac_toe import TicTacToe
import random

app2 = Flask(__name__)
object_list = {}


def game_messsage(i):
    return str(object_list[i].players[0])+"'s turn to play"


def play_message(i):
    return str(object_list[i].players[0])+"'s turn to play"


@app2.route('/display/<i>')
def display(i, message):
    x = 1 if object_list[i].is_relinquishing_starting_turn_possible() else 0
    return render_template('display1.html',
                           positions=object_list[i].positions,
                           message=message,
                           enable_switch=x,
                           no_of_rows=object_list[i].no_of_rows,
                           no_of_columns=object_list[i].no_of_columns,
                           user=i)


@app2.route("/reset/<i>", methods=['POST'])
def reset(i):
    object_list[i].reset()
    return display(i, message=play_message(i))

@app2.route("/switch/<i>", methods=['POST'])
def switch(i):
    if object_list[i].is_relinquishing_starting_turn_possible():
        object_list[i].relinquish_starting_turn()
    else:
        pass
    return display(i, message=play_message(i))


@app2.route("/<i>")
def index(i):
    return display(i, message=play_message(i))


@app2.route("/play/<i>", methods=['POST'])
def play(i):
    sub_value = request.form.get('sub')
    sub_value_int = int(sub_value)
    y1 = sub_value_int % 3
    x1 = sub_value_int // 3
    object_list[i].play(x1, y1)
    winner = object_list[i].get_winner()
    if winner is not None:
        return display(i, message=str(winner) + " has won")

    if object_list[i].is_game_draw():
        return display(i, message="it is a draw")

    return redirect(url_for("index", i=i))


@app2.route('/login', methods=['POST'])
def login():
    user = str(random.randint(1000, 9999))+"-"+str(random.randint(1000, 9999))
    if user not in object_list:
        object_list[user] = TicTacToe(user)
        return display(user, message=play_message(user))


@app2.route("/")
def checking():
    return render_template("home_page.html")


@app2.route("/temp", methods=['POST'])
def game_options():
    print(request.method)
    if request.method == 'POST':
        if request.form.get('Enter old room') == 'Enter old room':
            return old_room()
        elif request.form.get('Create new room') == 'Create new room':
            return login()


@app2.route('/oldroominput', methods=['POST'])
def oldroominput():
    if request.method == 'POST':
        i = request.form['nm']
        if i in object_list:
            return display(i, message=play_message(i))
        else:
            return "There is no such room"


@app2.route("/oldroom")
def old_room():
    return render_template("oldroom.html")


@app2.route("/home", methods=['POST'])
@app2.route("/home/<i>", methods=['POST'])
def backhome(i="hjgasg"):
    return checking()




app2.run()
