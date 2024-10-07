from pieces.Piece import Piece


class Pawn(Piece):
    def __init__(self, color, position):
        self.name = 'Pawn'
        super(Pawn, self).__init__(color, position)
        if self.color == 'w':
            self.image = 'images/white_pawn.png'
        else:
            self.image = 'images/black_pawn.png'

        self.value = 1

    def get_possible_moves(self, board):
        moves = []

        if not self.is_piece_in_front(board):
            moves.append((self.position[0], self.position[1] + self.direction))

            if (not self.has_moved) and (not board[self.position[0]][self.position[1] + 2 * self.direction]):
                moves.append((self.position[0], self.position[1] + 2 * self.direction))

        if self.position[0] < 7:
            right_diagonal = board[self.position[0] + 1][self.position[1] + self.direction]
            if right_diagonal and self.is_opponent(right_diagonal):
                moves.append(right_diagonal.position)

        if self.position[0] > 0:
            left_diagonal = board[self.position[0] - 1][self.position[1] + self.direction]
            if left_diagonal and self.is_opponent(left_diagonal):
                moves.append(left_diagonal.position)

        return moves

    def is_piece_in_front(self, board):
        return board[self.position[0]][self.position[1] + self.direction]

    def is_opponent_piece_diagonal(self, board, left_side):
        side = -1 if left_side else 1
        return board[self.position[0] + side][self.position[1] + self.direction].color == self.opponent_color


