from pieces.Bishop import Bishop
from pieces.King import King
from pieces.Knight import Knight
from pieces.Pawn import Pawn
from pieces.Queen import Queen

from pieces.Rook import Rook


class ChessBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        for i in range(8):
            self.board[i][1] = Pawn('w', (i, 1))
            self.board[i][6] = Pawn('b', (i, 6))

        self.board[0][7] = Rook('b', (0, 7))
        self.board[7][7] = Rook('b', (7, 7))
        self.board[1][7] = Knight('b', (1, 7))
        self.board[6][7] = Knight('b', (6, 7))
        self.board[2][7] = Bishop('b', (2, 7))
        self.board[5][7] = Bishop('b', (5, 7))
        self.board[4][7] = King('b', (4, 7))
        self.board[3][7] = Queen('b', (3, 7))

        self.board[0][0] = Rook('w', (0, 0))
        self.board[7][0] = Rook('w', (7, 0))
        self.board[1][0] = Knight('w', (1, 0))
        self.board[6][0] = Knight('w', (6, 0))
        self.board[2][0] = Bishop('w', (2, 0))
        self.board[5][0] = Bishop('w', (5, 0))
        self.board[4][0] = King('w', (4, 0))
        self.board[3][0] = Queen('w', (3, 0))

        self.curr_player = 'w'

        self.played_moves = []

    def get_all_pieces(self):
        """Returns list of all pieces on board"""
        pieces = []
        for x in range(8):
            for y in range(8):
                if self.board[x][y]:
                    pieces.append(self.board[x][y])
        return pieces

    def get_curr_player_pieces(self):
        """Returns all remaining pieces of current player"""
        pieces = []
        for piece in self.get_all_pieces():
            if piece.color == self.curr_player:
                pieces.append(piece)
        return pieces

    def get_poss_moves_for(self, piece):
        """Returns all possible moves for piece given"""
        # NOTE: Must check for a Castle move if king is selected
        if piece.name != 'King':
            return piece.get_possible_moves(self.board)
        else:
            return piece.get_possible_moves(self.board) + self.get_castle_moves_for_curr_player()

    def get_piece_at(self, space):
        """Returns piece at space"""
        return self.board[space[0]][space[1]]

    def get_type_pieces_of_player(self, piece_name, player):
        """Returns all pieces of type given of player given"""
        pieces = []
        for row in self.board:
            for space in row:
                if space and space.name == piece_name and space.color == player:
                    pieces.append(space)
        return pieces

    def move_piece(self, piece, new_position):
        """Moves piece to new position AND changes has_moved to TRUE
        Returns piece if piece taken, none if not"""
        pos = piece.position
        piece_to_take = self.board[new_position[0]][new_position[1]]
        piece.move(new_position)
        self.board[new_position[0]][new_position[1]] = piece
        self.board[pos[0]][pos[1]] = None
        if not piece.has_moved:
            piece.has_moved = True

        if piece_to_take:
            return piece_to_take
        return None

    def non_permanent_move(self, piece, new_position):
        """Moves piece and does NOT change has_moved to true. Used to check for checks/checkmates"""
        pos = piece.position
        piece.move(new_position)
        self.board[new_position[0]][new_position[1]] = piece
        self.board[pos[0]][pos[1]] = None

    def get_castle_moves_for_curr_player(self):
        """Returns list of possible castle positions"""
        castles = []
        king = self.get_type_pieces_of_player('King', self.curr_player)[0]
        y = 0 if self.curr_player == 'w' else 7
        b = self.board
        # Check king and rook have not moved
        if b[0][y] and not b[0][y].has_moved and b[4][y] and not b[4][y].has_moved:
            # Check no pieces in between rook and king
            if all(not b[x][y] for x in range(1, 4)):
                if not self.king_in_check(king, self.board):
                    castles.append((2, y))

        if b[7][y] and not b[7][y].has_moved and b[4][y] and not b[4][y].has_moved:
            if all(not b[x][y] for x in range(5, 7)):
                if not self.king_in_check(king, self.board):
                    castles.append((6, y))

        # Simulate both moves and check player is in check
        for move in castles:
            self.non_permanent_castle_king(king, move)
            if self.king_in_check(king, self.board):
                castles.remove(move)
            # Uncastle pieces
            self.uncastle_king(king)

        return castles

    def castle_king(self, king, new_king_position):
        """Given king piece and one of the four king positions that can make a castle. Moves king to that position and
        moves corresponding rook as well"""
        # NEW_KING_POS = (2, 0), (6, 0), (2, 7), (6, 7)
        corresponding_rook = {(2, 0): (0, 0), (6, 0): (7, 0), (2, 7): (0, 7), (6, 7): (7, 7)}
        corresponding_rook_move = {(2, 0): (3, 0), (6, 0): (5, 0), (2, 7): (3, 7), (6, 7): (5, 7)}
        rook_pos = corresponding_rook[new_king_position]
        rook = self.board[rook_pos[0]][rook_pos[1]]
        self.move_piece(king, new_king_position)
        self.move_piece(rook, corresponding_rook_move[new_king_position])

    def non_permanent_castle_king(self, king, new_king_position):
        """Given king piece and one of the four king positions that can make a castle. Moves king to that position and
        moves corresponding rook as well. DOES NOT change piece has_moved"""
        # NEW_KING_POS = (2, 0), (6, 0), (2, 7), (6, 7)
        corresponding_rook = {(2, 0): (0, 0), (6, 0): (7, 0), (2, 7): (0, 7), (6, 7): (7, 7)}
        corresponding_rook_move = {(2, 0): (3, 0), (6, 0): (5, 0), (2, 7): (3, 7), (6, 7): (5, 7)}
        rook_pos = corresponding_rook[new_king_position]
        rook = self.board[rook_pos[0]][rook_pos[1]]
        self.non_permanent_move(king, new_king_position)
        self.non_permanent_move(rook, corresponding_rook_move[new_king_position])

    def uncastle_king(self, king):
        """Reverts a castle move"""
        corresponding_rook = {(2, 0): (3, 0), (6, 0): (5, 0), (2, 7): (3, 7), (6, 7): (5, 7)}
        corresponding_rook_move = {(2, 0): (0, 0), (6, 0): (7, 0), (2, 7): (0, 7), (6, 7): (7, 7)}
        rook_pos = corresponding_rook[king.position]
        rook = self.board[rook_pos[0]][rook_pos[1]]
        self.non_permanent_move(rook, corresponding_rook_move[king.position])
        self.non_permanent_move(king, (4, king.position[1]))


    def king_in_check(self, king, b):
        """Returns if king is currently in check given board"""
        # Check for bishop or queen in diagonal path of king
        for m in king.get_possible_diagonal_moves(b):
            if b[m[0]][m[1]] and b[m[0]][m[1]].name in ['Bishop', 'Queen']:
                return True

        # Check for rook or queen in straight path of king
        for m in king.get_possible_straight_line_moves(b):
            if b[m[0]][m[1]] and b[m[0]][m[1]].name in ['Rook', 'Queen']:
                return True

        # Check for opponent king next to current king
        for m in king.get_possible_moves(b):
            if b[m[0]][m[1]] and b[m[0]][m[1]].name == 'King':
                return True

        # Check for opponent knights
        for m in [(1, 2), (2, 1), (-1, 2), (-2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1)]:
            pos = king.position[0] + m[0], king.position[1] + m[1]
            if pos[0] < 0 or pos[0] > 7 or pos[1] < 0 or pos[1] > 7:
                continue
            if b[pos[0]][pos[1]] and b[pos[0]][pos[1]].name == 'Knight' \
                    and b[pos[0]][pos[1]].color != self.curr_player:
                return True

        # Check for opponent pawns
        y_dir = 1 if self.curr_player == 'w' else -1
        # Check diagonals
        l_diag = king.position[0] - 1, king.position[1] + y_dir
        r_diag = king.position[0] + 1, king.position[1] + y_dir

        if l_diag[0] >= 0:
            if b[l_diag[0]][l_diag[1]] and b[l_diag[0]][l_diag[1]].name == 'Pawn' and b[l_diag[0]][l_diag[1]].color != self.curr_player:
                return True
        if r_diag[0] <= 7:
            if b[r_diag[0]][r_diag[1]] and b[r_diag[0]][r_diag[1]].name == 'Pawn' and b[r_diag[0]][r_diag[1]].color != self.curr_player:
                return True

    def is_curr_player_in_check(self, piece, moves):
        """Returns list of valid moves that don't put player in check. """
        king = self.get_type_pieces_of_player('King', self.curr_player)[0]
        b = self.board
        piece_original_pos = piece.position

        poss_moves = []

        for move in moves:
            # Move piece to new move
            piece_at_move_pos = self.board[move[0]][move[1]]
            self.non_permanent_move(piece, move)

            if not self.king_in_check(king, b):
                poss_moves.append(move)

            # Move piece back to original position
            self.non_permanent_move(piece, piece_original_pos)
            self.board[move[0]][move[1]] = piece_at_move_pos

        return poss_moves
