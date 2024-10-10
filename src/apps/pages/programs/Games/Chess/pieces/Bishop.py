from pieces.Piece import Piece


class Bishop(Piece):
    def __init__(self, color, position):
        self.name = 'Bishop'
        super(Bishop, self).__init__(color, position)
        if self.color == 'w':
            self.image = 'images/white_bishop.png'
        else:
            self.image = 'images/black_bishop.png'

        self.value = 3

    def get_possible_moves(self, board):
        return self.get_possible_diagonal_moves(board)