from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import jwt

from tic_tac_toe import TicTacToe
import random

app2 = Flask(__name__)
CORS(app2)

rooms = {}


def conclusion(room, identity):
    return {'board': room.positions,
            'player_to_play': room.player_to_play(),
            "is_draw": room.is_game_draw(),
            "who_won": room.get_winner(),
            "id": identity
            }


secret = "secretxyz"


def get_claim(r):
    authorization_value = r.headers.get('Authorization')
    try:
        return jwt.decode(authorization_value[7:], secret, verify=True, algorithm="HS256")
    except Exception as e:
        print(e)
        return None


def create_random_string():
    return str(random.randint(100, 999)) + "-" + str(random.randint(100, 999))


def get_token(room_id, player):
    x = jwt.encode({"room_id": room_id, "player": player}, secret, algorithm="HS256").decode("UTF-8")
    return x


@app2.route('/games', methods=["POST"])
def create_game():
    room_id = create_random_string()
    while room_id in rooms.keys():
        room_id = create_random_string()
    rooms[room_id] = TicTacToe(room_id)
    return jsonify({'room_id': room_id, "token": get_token(room_id, 'x')}), 202


@app2.route('/games/<string:room_id>')
def get_game(room_id):
    claim = get_claim(request)
    if claim is None or room_id != claim["room_id"]:
        return {'error': "access denied"}, 401
    if room_id not in rooms.keys():
        return {'error': "room id not found"}, 404
    room = rooms[room_id]
    return jsonify(conclusion(room, claim["player"]))


@app2.route('/games/<string:room_id>/reset', methods=['POST'])
def reset_game(room_id):
    claim = get_claim(request)
    if claim is None or room_id != claim["room_id"]:
        return {'error': "access denied"}, 401
    if room_id not in rooms.keys():
        return {'error': "room id not found"}, 404
    room = rooms[room_id]
    room.reset()
    return jsonify(conclusion(room, claim["player"]))


@app2.route('/games/<string:room_id>/play', methods=['POST'])
def play_game(room_id):
    claim = get_claim(request)
    if claim is None or room_id != claim["room_id"]:
        return {'error': "access denied"}, 401
    if room_id not in rooms.keys():
        return {'error': "room id not found"}, 404
    room = rooms[room_id]
    if room.player_to_play() == claim["player"]:
        payload = request.get_json()
        cell = payload['cell']
        y = cell % 3
        x = cell // 3
        room.play(x, y)
        return jsonify(conclusion(room, claim["player"]))
    return {'error': "not your turn to play"}, 403


@app2.route('/games/<string:room_id>/relinquish-first-turn', methods=['POST'])
def relinquish_first_turn(room_id):
    claim = get_claim(request)
    if claim is None or room_id != claim["room_id"]:
        return {'error': "access denied"}, 401
    if room_id not in rooms.keys():
        return {'error': "room id not found"}, 404
    room = rooms[room_id]
    if room.is_relinquishing_starting_turn_possible():
        room.relinquish_starting_turn()
        return jsonify(conclusion(room, claim["player"]))
    return {'error': "unable to relinquish turn"}, 403


@app2.route("/games/<room_id>/join", methods=['POST'])
def join_room(room_id):
    if room_id not in rooms.keys():
        return {'error': "room id not found"}, 404
    return jsonify({"token": get_token(room_id, 'o')})


@app2.route("/")
def home():
    return render_template("home_page.html")


@app2.route("/ui/games/<string:id>")
def game(id):
    return render_template("game.html", room_id=id)


if __name__ == '__main__':
    app2.run(debug=True, host='0.0.0.0', port=80)
