class Piece:
    def __init__(self, color, position):
        self.name
        self.position = position
        self.color = color.lower()
        self.opponent_color = 'b' if self.color == 'w' else 'w'
        if color not in ['b', 'w']:
            raise TypeError('%s color should be \'w\' or \'b\'' % self.name)

        self.direction = 1 if self.color == 'w' else -1
        self.has_moved = False
        self.turn_first_moved = 0

    def get_possible_moves(self, board):
        return []

    def can_move(self, move, board):
        return move in self.get_possible_moves(board)

    def move(self, move):
        self.position = move

    def is_opponent(self, piece):
        return piece.color == self.opponent_color

    def get_possible_straight_line_moves(self, board):
        # Does not affect anything. Returns list of moves
        moves = []
        curr_pos = self.position[0], self.position[1] + 1
        while curr_pos[1] <= 7:
            piece = board[curr_pos[0]][curr_pos[1]]
            if not piece:
                moves.append(curr_pos)
            elif self.is_opponent(piece):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0], curr_pos[1] + 1

        curr_pos = self.position[0], self.position[1] - 1
        while curr_pos[1] >= 0:
            piece = board[curr_pos[0]][curr_pos[1]]
            if not piece:
                moves.append(curr_pos)
            elif self.is_opponent(piece):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0], curr_pos[1] - 1

        curr_pos = self.position[0] + 1, self.position[1]
        while curr_pos[0] <= 7:
            piece = board[curr_pos[0]][curr_pos[1]]
            if not piece:
                moves.append(curr_pos)
            elif self.is_opponent(piece):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0] + 1, curr_pos[1]

        curr_pos = self.position[0] - 1, self.position[1]
        while curr_pos[0] >= 0:
            piece = board[curr_pos[0]][curr_pos[1]]
            if not piece:
                moves.append(curr_pos)
            elif self.is_opponent(piece):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0] - 1, curr_pos[1]

        return moves

    def get_possible_diagonal_moves(self, board):
        # Does not affect anything. Returns list of moves
        moves = []
        curr_pos = self.position[0] + 1, self.position[1] + 1
        while curr_pos[1] <= 7 and curr_pos[0] <= 7:
            piece = board[curr_pos[0]][curr_pos[1]]
            if not piece:
                moves.append(curr_pos)
            elif self.is_opponent(piece):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0] + 1, curr_pos[1] + 1

        curr_pos = self.position[0] + 1, self.position[1] - 1
        while curr_pos[1] >= 0 and curr_pos[0] <= 7:
            piece = board[curr_pos[0]][curr_pos[1]]
            if not piece:
                moves.append(curr_pos)
            elif self.is_opponent(piece):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0] + 1, curr_pos[1] - 1

        curr_pos = self.position[0] - 1, self.position[1] + 1
        while curr_pos[0] >= 0 and curr_pos[1] <= 7:
            piece = board[curr_pos[0]][curr_pos[1]]
            if not piece:
                moves.append(curr_pos)
            elif self.is_opponent(piece):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0] - 1, curr_pos[1] + 1

        curr_pos = self.position[0] - 1, self.position[1] - 1
        while curr_pos[1] >= 0 and curr_pos[0] >= 0:
            piece = board[curr_pos[0]][curr_pos[1]]
            if not piece:
                moves.append(curr_pos)
            elif self.is_opponent(piece):
                moves.append(curr_pos)
                break
            else:
                break

            curr_pos = curr_pos[0] - 1, curr_pos[1] - 1

        return moves