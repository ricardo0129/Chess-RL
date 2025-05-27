from enum import Enum

PIECE_SYMBOLS = [' ', '♙', '♞', '♗', '♖', '♕', '♔']

WHITE = '\033[97m'
BLACK = '\033[91m'
RESET = '\033[0m'

class PieceType(Enum):
    EMPTY = 0
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6
    
def piece_symbol(piece_type: PieceType) -> str:
    return PIECE_SYMBOLS[piece_type.value]

class Color(Enum):
    EMPTY = -1
    WHITE = 0
    BLACK = 1

PIECE_COLORS = {
        Color.EMPTY: '',
        Color.WHITE: WHITE,
        Color.BLACK: BLACK,
}

class Piece:
    def __init__(self, piece_type: PieceType, color: Color):
        self.piece_type = piece_type
        self.color = color
        self.has_moved = False
        self.last_position = None

    def __str__(self):
        return f'{PIECE_COLORS[self.color]}{piece_symbol(self.piece_type)}{RESET}'

    def __repr__(self):
        return str(self)


front_row = [PieceType.ROOK, PieceType.KNIGHT, PieceType.BISHOP, PieceType.QUEEN, PieceType.KING, PieceType.BISHOP, PieceType.KNIGHT, PieceType.ROOK]
back_row  = [PieceType.PAWN] * 8

class Move():
    def __init__(self, start: tuple[int, int], end: tuple[int, int]):
        self.start = start
        self.end = end

    def __str__(self):
        return f"{self.start}->{self.end}"

    def __repr__(self):
        return str(self)

class Board:
    def __init__(self):
        self.board = [[Piece(PieceType.EMPTY, Color.EMPTY) for _ in range(8)] for _ in range(8)]
        for i in range(8):
            self.board[0][i] = Piece(front_row[i], Color.BLACK)
            self.board[1][i] = Piece(back_row[i], Color.BLACK)

            self.board[6][i] = Piece(back_row[i], Color.WHITE)
            self.board[7][i] = Piece(front_row[i], Color.WHITE)

    def __getitem__(self, square: tuple[int, int]) -> Piece:
        assert 0 <= square[0] < 8 and 0 <= square[1] < 8, "Square out of bounds"
        return self.board[square[0]][square[1]]

    def __setitem__(self, square: tuple[int, int], piece: Piece):
        assert 0 <= square[0] < 8 and 0 <= square[1] < 8, "Square out of bounds"
        self.board[square[0]][square[1]] = piece

    def __str__(self):
        board_str = ""
        for row in self.board:
            board_str += " | ".join(str(piece) for piece in row) + "\n"
        return board_str

def valid_rook_moves(square: tuple[int, int], board: 'Board') -> list[tuple[int, int]]:
    moves = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # Right, Left, Down, Up
    for dx, dy in directions:
        x, y = square
        while True:
            x += dx
            y += dy
            if not (0 <= x < 8 and 0 <= y < 8):
                break
            if board[x, y].piece_type == PieceType.EMPTY:
                moves.append((x, y))
            elif board[x, y].color != board[square].color:
                moves.append((x, y))
                break
            else:
                break
    return moves
def valid_knight_moves(square: tuple[int, int], board: 'Board') -> list[tuple[int, int]]:
    moves = []
    knight_moves = [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]
    for dx, dy in knight_moves:
        new_square = (square[0] + dx, square[1] + dy)
        if inside_board(new_square) and (board[new_square].piece_type == PieceType.EMPTY or board[new_square].color != board[square].color):
            moves.append(new_square)
    return moves
def inside_board(square: tuple[int, int]) -> bool:
    return 0 <= square[0] < 8 and 0 <= square[1] < 8

def valid_pawn_moves(square: tuple[int, int], board: 'Board') -> list[tuple[int, int]]:
    moves = []
    piece = board[square]
    direction = -1 if piece.color == Color.WHITE else 1
    if not piece.has_moved:
        moves.append((square[0] + direction * 2, square[1]))
    forward_pos = (square[0] + direction, square[1])
    if inside_board(forward_pos) and board[forward_pos].piece_type == PieceType.EMPTY:
        moves.append(forward_pos)
    for dy in [-1, 1]:
        diagonal_pos = (square[0] + direction, square[1] + dy)
        if inside_board(diagonal_pos) and board[diagonal_pos].piece_type != PieceType.EMPTY and board[diagonal_pos].color != piece.color:
            moves.append(diagonal_pos)

    # Add en passant logic here
    for dy in [-1, 1]:
        en_passant_pos = (square[0], square[1] + dy)
        if inside_board(en_passant_pos) and board[en_passant_pos].piece_type == PieceType.PAWN and board[en_passant_pos].color != piece.color:
            if board[en_passant_pos].has_moved:

    return moves



def valid_moves(square: tuple[int, int], board: Board) -> list[Move]:
    piece = board[square]
    if piece.piece_type == PieceType.EMPTY:
        return []
    
    moves = []
    if piece.piece_type == PieceType.ROOK:
        for move in valid_rook_moves(square, board):
            moves.append(Move(square, move))
    elif piece.piece_type == PieceType.PAWN:
        for move in valid_pawn_moves(square, board):
            moves.append(Move(square, move))
    # Add logic for other pieces here (e.g., knight, bishop, etc.)
    
    return moves

class Game:
    def __init__(self):
        self.board = Board()
        self.moves = []
        self.current_turn = Color.WHITE

    def make_move(self, move: Move):
        # Logic to make a move on the board
        self.moves.append(move)
        start_piece = self.board[move.start]
        end_piece = self.board[move.end]
        if not inside_board(move.start) or not inside_board(move.end):
            raise ValueError("Move out of bounds")
        if start_piece.piece_type == PieceType.EMPTY:
            raise ValueError("No piece at start square")
        if start_piece.color != self.current_turn:
            raise ValueError("It's not your turn")
        if move.end not in valid_moves(move.start, self.board):
            raise ValueError("Invalid move for the piece")
        # Validated its a valid move, and you are moving your piece, and nothing is out of bounds
        self.board[move.end] = start_piece
        self.board[move.start] = Piece(PieceType.EMPTY, Color.EMPTY)
        start_piece.has_moved = True
        # Switch turns
        self.current_turn = Color.BLACK if self.current_turn == Color.WHITE else Color.WHITE
        print(f"Moved {start_piece} from {move.start} to {move.end}")

    def valid_moves(self, square: tuple[int, int]) -> list[Move]:
        # Logic to find valid moves for a piece at the given square
        if self.board[square].piece_type == PieceType.EMPTY or self.board[square].color != self.current_turn:
            return []
        return valid_moves(square, self.board)

    def __str__(self):
        return str(self.board)

game = Game()
print(game)
print(game.valid_moves((6, 0)))  # Example to get valid moves for a piece at (5, 0)
