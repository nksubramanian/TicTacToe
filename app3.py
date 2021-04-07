from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_cors import CORS

from tic_tac_toe import TicTacToe
import random

app2 = Flask(__name__)
CORS(app2)

rooms = {}


def conclusion(room):
    return {'board': room.positions,
            'player_to_play': room.player_to_play(),
            "is_draw": room.is_game_draw(),
            "who_won": room.get_winner()
            }


def create_random_string():
    return str(random.randint(100, 999)) + "-" + str(random.randint(100, 999))


@app2.route('/games', methods=["POST"])
def create_game():
    room_id = create_random_string()
    while room_id in rooms.keys():
        room_id = create_random_string()
    rooms[room_id] = TicTacToe(room_id)
    return jsonify({'room_id': room_id, "token": "helloworldxyz"}), 202


@app2.route('/games/<string:room_id>')
def get_game(room_id):
    if room_id not in rooms.keys():
        return {'error': "room id not found"}, 404
    room = rooms[room_id]
    return jsonify(conclusion(room))

    #status of the game (in progress, won, draw)
    #Winner


@app2.route('/games/<string:room_id>/reset', methods=['POST'])
def reset_game(room_id):
    authorization_value = request.headers.get('Authorization')
    if authorization_value is None or "Bearer" not in authorization_value:
        return {'error': "access denied"}, 401
    print("Authorization succeeded")
    if room_id not in rooms.keys():
        return {'error': "room id not found"}, 404
    room = rooms[room_id]
    room.reset()
    return jsonify(conclusion(room))


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
    return jsonify(conclusion(room))


@app2.route('/games/<string:room_id>/relinquish-first-turn', methods=['POST'])
def relinquish_first_turn(room_id):
    if room_id not in rooms.keys():
        return {'error': "room id not found"}, 404
    room = rooms[room_id]
    if room.is_relinquishing_starting_turn_possible():
        room.relinquish_starting_turn()
        return jsonify(conclusion(room))
    return {'error': "unable to relinquish turn"}, 400


@app2.route("/")
def home():
    return render_template("home_page.html")


@app2.route("/ui/games/<string:id>")
def game(id):
    return render_template("game.html", room_id=id)


@app2.route("/games/<room_id>/join", methods=['POST'])
def tokenreturn(room_id):
    return jsonify({"token": "helloworldabc"})


if __name__ == '__main__':
    app2.run(debug=True, host='0.0.0.0', port=80)

