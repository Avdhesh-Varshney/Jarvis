from pieces.Piece import Piece


class Knight(Piece):
    def __init__(self, color, position):
        self.name = 'Knight'
        super(Knight, self).__init__(color, position)
        if self.color == 'w':
            self.image = 'images/white_knight.png'
        else:
            self.image = 'images/black_knight.png'

        self.value = 3

    def get_possible_moves(self, board):
        poss_moves = [(1, 2), (2, 1), (-1, 2), (-2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]
        moves = []
        for move in poss_moves:
            pos = self.position[0] + move[0], self.position[1] + move[1]
            if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
                continue
            piece = board[pos[0]][pos[1]]
            if not piece or self.is_opponent(piece):
                moves.append(pos)
        return moves