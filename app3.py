from flask import Flask, request, render_template, redirect, url_for, jsonify
from tic_tac_toe import TicTacToe
import random

app2 = Flask(__name__)
rooms = {}


def create_random_string():
    return str(random.randint(100, 999)) + "-" + str(random.randint(100, 999))


@app2.route('/games', methods=["POST"])
def create_game():
    room_id = create_random_string()
    while room_id in rooms.keys():
        room_id = create_random_string()
    rooms[room_id] = TicTacToe(room_id)
    return jsonify({'room_id': room_id}), 201


@app2.route('/games/<string:room_id>')
def get_game(room_id):
    if room_id not in rooms.keys():
        return {'error': "room id not found"}, 404
    room = rooms[room_id]
    return jsonify({'board': room.positions, 'player_to_play': room.players[0]})
    #status of the game (in progress, won, draw)
    #Winner


@app2.route('/games/<string:room_id>/reset', methods=['POST'])
def reset_game(room_id):
    if room_id not in rooms.keys():
        return {'error': "room id not found"}, 404
    room = rooms[room_id]
    room.reset()
    return jsonify({'board': room.positions, 'player_to_play': room.players[0]})


@app2.route('/games/<string:room_id>/play', methods=['POST'])
def play_game(room_id):
    if room_id not in rooms.keys():
        return {'error': "room id not found"}, 404
    room = rooms[room_id]
    payload = request.get_json()
    cell = payload['cell']
    y = cell % 3
    x = cell // 3
    room.play(x, y)
    return jsonify({'board': room.positions, 'player_to_play': room.players[0]})


@app2.route('/games/<string:room_id>/relinquish-first-turn', methods=['POST'])
def relinquish_first_turn(room_id):
    if room_id not in rooms.keys():
        return {'error': "room id not found"}, 404
    room = rooms[room_id]
    if room.is_relinquishing_starting_turn_possible():
        room.relinquish_starting_turn()
        return jsonify({'board': room.positions, 'player_to_play': room.players[0]})
    return {'error': "unable to relinquish turn"}, 400


@app2.route("/")
def home():
    return render_template("home_page.html")


@app2.route("/ui/games/<string:id>")
def game(id):
    return id

app2.run()