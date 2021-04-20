import jwt

class AuthorizationHandler:
    def __init__(self, secret):
        self.secret = secret

    def get_claim(self, authorization_value):
        try:
            return jwt.decode(authorization_value, self.secret, verify=True, algorithm="HS256")
        except Exception as e:
            return None

    def create_token(self, room_id, player):
        x = jwt.encode({"room_id": room_id, "player": player}, self.secret, algorithm="HS256").decode("UTF-8")
        return x
