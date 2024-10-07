from pieces.Piece import Piece


class Queen(Piece):
    def __init__(self, color, position):
        self.name = 'Queen'
        super(Queen, self).__init__(color, position)
        if self.color == 'w':
            self.image = 'images/white_queen.png'
        else:
            self.image = 'images/black_queen.png'

        self.value = 9

    def get_possible_moves(self, board):
        return self.get_possible_straight_line_moves(board) + self.get_possible_diagonal_moves(board)
