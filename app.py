from flask import Flask, request, render_template, jsonify
from flask_cors import CORS

from tic_tac_toe import TicTacToe
import random


def create_app(auth_handler):
    app = Flask(__name__)
    CORS(app)
    rooms = {} #db


    def get_game_status(room, identity):
        return {'board': room.positions,
                'player_to_play': room.player_to_play(),
                "is_draw": room.is_game_draw(),
                "who_won": room.get_winner(),
                "id": identity
                }

    def get_claim(r):
        authorization_value = r.headers.get('Authorization')
        authorization_value = authorization_value[7:]
        return auth_handler.get_claim(authorization_value)

    def create_token(room_id, player):
        auth_handler.create_token(room_id, player)

    def generate_room_id():
        return str(random.randint(100, 999)) + "-" + str(random.randint(100, 999))

    @app.route('/games', methods=["POST"])
    def create_game():
        room_id = generate_room_id()
        while room_id in rooms.keys():
            room_id = generate_room_id()
        rooms[room_id] = TicTacToe(room_id)
        return jsonify({'room_id': room_id, "token": create_token(room_id, 'x')}), 202


    @app.route('/games/<string:room_id>')
    def get_game(room_id):
        claim = get_claim(request)
        if claim is None or room_id != claim["room_id"]:
            return {'error': "access denied"}, 401
        if room_id not in rooms.keys():
            return {'error': "room id not found"}, 404
        room = rooms[room_id]
        return jsonify(get_game_status(room, claim["player"]))


    @app.route('/games/<string:room_id>/reset', methods=['POST'])
    def reset_game(room_id):
        claim = get_claim(request)
        if claim is None or room_id != claim["room_id"]:
            return {'error': "access denied"}, 401
        if room_id not in rooms.keys():
            return {'error': "room id not found"}, 404
        room = rooms[room_id]
        room.reset()
        return jsonify(get_game_status(room, claim["player"]))


    @app.route('/games/<string:room_id>/play', methods=['POST'])
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
            return jsonify(get_game_status(room, claim["player"]))
        return {'error': "not your turn to play"}, 403


    @app.route('/games/<string:room_id>/relinquish-first-turn', methods=['POST'])
    def relinquish_first_turn(room_id):
        claim = get_claim(request)
        if claim is None or room_id != claim["room_id"]:
            return {'error': "access denied"}, 401
        if room_id not in rooms.keys():
            return {'error': "room id not found"}, 404
        room = rooms[room_id]
        if room.player_to_play() == claim["player"]:
            if room.is_relinquishing_starting_turn_possible():
                room.relinquish_starting_turn()
                return jsonify(get_game_status(room, claim["player"]))
            return {'error': "unable to relinquish turn"}, 403


    @app.route("/games/<room_id>/join", methods=['POST'])
    def join_room(room_id):
        if room_id not in rooms.keys():
            return {'error': "room id not found"}, 404
        return jsonify({'room_id': room_id, "token": create_token(room_id, 'o')})



    @app.route("/")
    def home():
        return render_template("home_page.html")


    @app.route("/ui/games/<string:id>")
    def game(id):
        return render_template("game.html", room_id=id)

    return app




