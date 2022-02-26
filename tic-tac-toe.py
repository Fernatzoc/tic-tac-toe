import enum

class piece(enum.Enum):
    blank = 0
    x = 1
    O = 2

    def __str__(self, strRepr=[" ", "X", "O"]):
        return strRepr[self.value]


class ticTacToe():
    def __init__(self, board=[], turn=piece.x):
        if board == []:
            self.board = [x[:] for x in [[piece.blank] * 3] * 3]
            self.turn = piece.x
        else:
            self.board = board
            self.turn = turn
        self.winner = piece.blank

    def __setPiece(self, cor, val):
        self.board[cor[0]][cor[1]] = val

    def __isMoveValid(self, move):
        if move in self.getPossibleMoves():
            return True
        return False

    def getTurn(self):
        return self.turn

    def getBoard(self):
        return self.board

    def makeMove(self, move):
        if (self.__isMoveValid(move)):
            self.__setPiece(move, self.turn)
            for i in self.getWinConditions():
                if (self.getEqualsOnRow(i, self.turn)):
                    self.winner = self.turn
                    break
            self.turn = piece.x if (
                self.turn == piece.O) else piece.O
        else:
            return False
        return True

    def printBoard(self):
        print("- - - -")
        for row in self.board:
            rowStr = "|"
            for col in row:
                rowStr = rowStr + "%s|" % (str(col))
            print(rowStr)
            print("- - - -")

    def getGameFinished(self):
        if self.getPossibleMoves() == [] or self.winner != piece.blank:
            return True
        return False

    def getWinner(self):
        return self.winner

    def getPossibleMoves(self):
        moves = []
        for row in range(0, len(self.board)):
            for col in range(0, len(self.board[row])):
                if self.board[row][col] == piece.blank:
                    moves.append((row, col))
        return moves

    def getEqualsOnRow(self, row, piece):
        if ((self.board[row[0][0]][row[0][1]] == self.board[row[1][0]][row[1][1]]) and
            (self.board[row[0][0]][row[0][1]] == self.board[row[2][0]][row[2][1]]) and
                (self.board[row[0][0]][row[0][1]] == piece)):
            return True

        return False

    def evaluateBoard(self):

        if self.getWinner() == piece.x:
            return 10
        elif self.getWinner() == piece.O:
            return -10
        elif self.getPossibleMoves() == []:
            return 0

    def getWinConditions(self):
        winCond = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],

            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],

            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]
        ]

        return winCond


class minMaxAlgo():
    def getMove(self):
        return self.nextMove

    def performAlgo(self, board, depth, turn=piece.x):
        if (board.getGameFinished()) or (depth == 0):
            return board.evaluateBoard()

        arr = [row[:] for row in board.board]

        if turn == piece.x:
            maxVal = -11
            for moves in board.getPossibleMoves():
                cpyBoard = [row[:] for row in arr]
                newBoard = ticTacToe(cpyBoard, turn)
                newBoard.makeMove(moves)
                newVal = minMaxAlgo().performAlgo(newBoard, depth-1, newBoard.getTurn())
                if newVal > maxVal:
                    self.nextMove = moves
                    maxVal = newVal
            return maxVal
        elif turn == piece.O:
            minVal = 11
            for moves in board.getPossibleMoves():
                cpyBoard = [row[:] for row in arr]
                newBoard = ticTacToe(cpyBoard, turn)
                newBoard.makeMove(moves)
                newVal = minMaxAlgo().performAlgo(newBoard, depth-1, newBoard.getTurn())
                if newVal < minVal:
                    self.nextMove = moves
                    minVal = newVal

            return minVal


ticTac = ticTacToe()
while True:
    z = minMaxAlgo()
    tt = z.performAlgo(ticTac, 9)
    print("El valor del juego puede ser: %d" % (tt))
    print("El ordenador se mueve:")
    print(z.getMove())
    ticTac.makeMove(z.getMove())
    ticTac.printBoard()
    if ticTac.getGameFinished():
        break
    print("Movimientos posibles:")
    print(ticTac.getPossibleMoves())
    move = tuple(int(x.strip()) for x in input("Ingrese fila y columna: ").split(','))
    while not ticTac.makeMove(move):
        print("Movimiento inválido - inténtelo de nuevo!")
        move = tuple(int(x.strip())
                     for x in input("Ingrese fila y columna: ").split(','))
    ticTac.printBoard()
    if ticTac.getGameFinished():
        break

whoWon = ticTac.getWinner()
if whoWon == piece.x:
    print("El ordenador (X) ha ganado la partida!")
elif whoWon == piece.O:
    print("Error")
else:
    print("Empate")
