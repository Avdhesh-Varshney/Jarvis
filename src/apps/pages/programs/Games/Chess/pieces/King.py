from pieces.Piece import Piece


class King(Piece):
    def __init__(self, color, position):
        self.name = 'King'
        super(King, self).__init__(color, position)
        if self.color == 'w':
            self.image = 'images/white_king.png'
        else:
            self.image = 'images/black_king.png'

        self.value = 100

    def get_possible_moves(self, board):
        moves = []
        for i in range(-1, 2):
            for e in range(-1, 2):
                space = self.position[0] + e, self.position[1] + i
                if space[0] < 0 or space[0] > 7 or space[1] < 0 or space[1] > 7:
                    continue
                piece = board[space[0]][space[1]]
                if not piece or self.is_opponent(piece):
                    moves.append(space)

        return moves

    def is_opponent(self, piece):
        return piece.color == self.opponent_color
