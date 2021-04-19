# TicTacToe

## Intention
- The intention of this project is to build a two player tic-tac-toe that could be played over the internet 
- The code is developed using Python 3.9 using Virtual environment for package isolation
- The application is build using Flask (Other dependencies are in Requirements.txt)

## Getting Started


Create Game ('/games', methods=["POST"]) returns token and room_id. This token is for a room id and player "x"

GET Get game ('/games/<string:room_id>') This end point is to get the game in the room id. This returns the players id,
whether the game is draw, whose turn to play and who has won

Play (('/games/<string:room_id>/play', methods=['POST'])): Here in the body, player's move is sent-the cell position where the player decides to play. 
The Header has information of bearer token. 

Relinquish(('/games/<string:room_id>/relinquish-first-turn', methods=['POST'])): This endpoint has only bearer token passed in the header. 

Join Room("/games/<room_id>/join", methods=['POST']): This endpoint returns the room_id and token for player "o"


Reset('/games/<string:room_id>/reset', methods=['POST']): This endpoint is used to reset the game. 

