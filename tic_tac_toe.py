class TicTacToe:

    def __init__(self, room_id):
        self.room_id = room_id
        self.positions = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.players = ['x', 'o']
        self.no_of_rows = 3
        self.no_of_columns = 3

    def reset(self):
        self.positions = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.players = ['x', 'o']

    def relinquish_starting_turn(self):
        if self.is_relinquishing_starting_turn_possible():
            self.players.reverse()
        else:
            raise Exception("Unsupported Operation relinquishing")

    def is_relinquishing_starting_turn_possible(self):
        for row in self.positions:
            for element in row:
                if element != 0:
                    return False
        return True

    def play(self, x, y):
        self.positions[x][y] = self.players[0]
        self.players.reverse()
        #have to validate if cell is already played

    def who_won_with_pattern(self, pattern):
        x1, y1 = pattern[0]
        val = self.positions[x1][y1]
        if val == 0:
            return None
        for (x, y) in pattern:
            if val != self.positions[x][y]:
                return None
        return val

    def get_winner(self):
        winning_patterns = [[(0, 0), (1, 1), (2, 2)],
                            [(0, 0), (0, 1), (0, 2)],
                            [(1, 0), (1, 1), (1, 2)],
                            [(2, 0), (2, 1), (2, 2)],
                            [(0, 0), (1, 0), (2, 0)],
                            [(0, 1), (1, 1), (2, 1)],
                            [(0, 2), (1, 2), (2, 2)],
                            [(0, 2), (1, 1), (2, 0)]]

        for pattern in winning_patterns:
            winner = self.who_won_with_pattern(pattern)
            if winner is not None:
                return winner
        return None

    def is_game_draw(self):
        for rows in self.positions:
            for element in rows:
                if element == 0:
                    return False
        return True