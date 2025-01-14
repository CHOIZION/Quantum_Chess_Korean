import Position
import Piece
import Move
import random
from utils import ChessUtils

class Game:
    def __init__(self):
        self.QMovesAllowed = 3
        self.QMovesWhite = 0
        self.QMovesBlack = 0
        self.position = Position.Position(self.setInitPieces())
        self.moveList = []
        self.flags = "w KQkq - 0 1"
        self.flagList = self.flags.split()
        self.linked = []

        self.over = False

    def setInitPieces(self, board = ["rnbqkbnr", "pppppppp", "........", "........", "........", "........", "PPPPPPPP", "RNBQKBNR"]):

        pieceMatrix = []
        row = 0
        while row < 8:
            col = 0
            rowList = []
            while col < 8:
                if board[row][col] != ".":
                    piece = Piece.Piece(board[row][col])
                    rowList.append(piece)
                else:
                    rowList.append(None)
                col += 1
            pieceMatrix.append(rowList)
            row += 1
        return pieceMatrix
    
    def setPosition(self, position):

        self.position = position
    
    def move(self, moveStr):

        move = Move.Move(moveStr, self.flagList)
        piece = self.position.getWhatIsOnSquare(move.move[0:2])
        if move.isValid(self.position):
            interferencers = list(set(ChessUtils.getInterference(self.position, move.move)))
            if move.isCapture(self.position):
                capturer = piece
                captured = self.position.getWhatIsOnSquare(move.move[2:4])
                
                for indexMove in interferencers:
                    choice = random.randint(0, 1)
                    self.position = self.position.mergePosition(indexMove, choice)
                    if self.moveList[indexMove].move0.flags[0] == "w":
                        self.QMovesWhite -=1
                    else:
                        self.QMovesBlack -=1

                if capturer.isQuantic():
                    listToMerge = self.getListToMerge(moveStr[0:2], capturer)
                    for indexMove in listToMerge:
                        choice = random.randint(0, 1)
                        self.position = self.position.mergePosition(indexMove, choice)
                        if self.flagList[0] == "w":
                            self.QMovesWhite -=1
                        else:
                            self.QMovesBlack -=1
                if captured == None:
                    if move.move[3] == "6" and move.move[1] == "5":
                        captured = self.position.getWhatIsOnSquare(move.move[2] + str(5))
                    if move.move[3] == "3" and move.move[1] == "4":
                        captured = self.position.getWhatIsOnSquare(move.move[2] + str(4))
                if captured.isQuantic():
                    listToMerge = self.getListToMerge(moveStr[2:4], captured)
                    for indexMove in listToMerge:
                        choice = random.randint(0, 1)
                        self.position = self.position.mergePosition(indexMove, choice)
                        if self.flagList[0] == "b":
                            self.QMovesWhite -=1
                        else:
                            self.QMovesBlack -=1
            if move.isValid(self.position):
                self.position = self.position.makeMove(move)
            self.moveList.append(move)
            
            self.flagList[0] = "w" if self.flagList[0] == "b" else "b" if self.flagList[0] == "w" else self.flagList[0]
            self.updateFlags(move, piece.pieceClass)
            self.link(move)
            self.deQuantify()
            return True
        else:
            print("불가능")
            return False

    def getListToMerge(self, sq, piece):

        listMerged = []
        for links in self.linked:
            if sq in links:
                for squareLinked in links:
                    piece = self.position.getWhatIsOnSquare(squareLinked)
                    if isinstance(piece, Piece.Piece):
                        listMerged = list(set(listMerged) | set(piece.listMoves))
        return listMerged


    def qMove(self, moveStr0, moveStr1):

        move0 = Move.Move(moveStr0, self.flagList)
        move1 = Move.Move(moveStr1, self.flagList)
        qMove = Move.QuanticMove(move0, move1)
        piece = self.position.getWhatIsOnSquare(moveStr0[0:2])
        if qMove.isValid(self.position):
            if (self.flagList[0] == "w" and self.QMovesWhite < self.QMovesAllowed):
                self.setPosition(self.position.makeMove(qMove))
                self.position.addToAllOnSquare(moveStr0[2:4], ([len(self.moveList)]))
                self.position.addToAllOnSquare(moveStr1[2:4], ([len(self.moveList)]))
                self.QMovesWhite += 1
                self.flagList[0] = "b"
                self.moveList.append(qMove)
                self.updateFlags(qMove, piece.pieceClass)
                self.deQuantify()
                self.link(qMove)
                self.linked.append([moveStr0[2:4], moveStr1[2:4]])
                return True
            elif(self.flagList[0] == "w" and self.QMovesWhite >= self.QMovesAllowed):
                print("양자 이동 불가능")
                return False
            if (self.flagList[0] == "b" and self.QMovesBlack < self.QMovesAllowed):
                self.setPosition(self.position.makeMove(qMove))
                self.position.addToAllOnSquare(moveStr0[2:4], ([len(self.moveList)]))
                self.position.addToAllOnSquare(moveStr1[2:4], ([len(self.moveList)]))
                self.QMovesBlack += 1
                self.flagList[0] = "w"
                self.moveList.append(qMove)
                self.updateFlags(qMove, piece.pieceClass)
                self.deQuantify()
                self.link(qMove)
                self.linked.append([moveStr0[2:4], moveStr1[2:4]])

                return True
            elif(self.flagList[0] == "b" and self.QMovesBlack >= self.QMovesAllowed):
                print("양자 이동 불가능")
                return False
        else:
            print("불가능")
            return False
        
    def link(self, move):

        if move.isQuantic():
            self.link(move.move0)
            self.link(move.move1)
        else:
            for i in range(len(self.linked)):  
                objective = move.move[0:2]
                subs = move.move[2:4]
                if objective in self.linked[i]:
                    self.linked[i][self.linked[i].index(objective)] = subs

    def deQuantify(self):

        isWhiteAlive = False
        isBlackAlive = False
        for row in range(8):
            for col in range(8):
                piece = self.position.deQuantify(row, col)
                if piece != None:
                    if piece.pieceClass in "k":
                        isBlackAlive = True
                    if piece.pieceClass in "K":
                        isWhiteAlive = True
                    if not piece.isQuantic():
                        square = ""
                        square += chr(col + ord('a'))
                        square += str(row + 1)
                        self.position.setPiece(piece, square)
        if not isWhiteAlive:
            self.over = "블랙 승리!"
        if not isBlackAlive:
            self.over = "화이트 승리!"

    def updateFlags(self, move, piece):

        if piece == "K":
            self.flagList[1].replace("KQ", "")
        if piece == "k":
            self.flagList[1].replace("kq", "")
        if (isinstance(move, Move.QuanticMove)):
            if move.move1.move[3] =="4":
                squares = move.move0.move
            else:
                squares = move.move1.move
        else:
            squares = move.move[0:4]
        if squares[0:2] == "a1":
            self.flagList[1].replace("Q", "")
        if squares[0:2] == "h1":
            self.flagList[1].replace("K", "")
        if squares[0:2] == "a8":
            self.flagList[1].replace("q", "")
        if squares[0:2] == "h8":
            self.flagList[1].replace("k", "")
        if piece == "P" and int(squares[1]) - int(squares[3]) == -2:
            self.flagList[2] = squares[0] + str(3)
        elif piece == "p" and int(squares[1]) - int(squares[3]) == 2:
            self.flagList[2] = squares[0] + str(6)
        else:
            self.flagList[2] == "-"

        if piece in "Pp":
            if (piece.islower() and squares[3] == '1') or ((piece.isupper()) and squares[3] == '8'):
                promoted = self.position.getWhatIsOnSquare(squares[2:4])
                if move.flags[0] == "b":
                    promoted.pieceClass = move.move[4].upper()
                else:
                    promoted.pieceClass = move.move[4].lower()

    def evaluate(self, movestr0 =0, movestr1 = 0):

        timeOut = 10
        if movestr1 != 0:
            move = Move.QuanticMove(Move.Move(movestr0, self.flagList), Move.Move(movestr1, self.flagList))
            return ChessUtils.evalMoveFormula(self.position, self.flagList, move, timeOut)
        elif movestr0 != 0:
            move = Move.Move(movestr0, self.flagList)
            return ChessUtils.evalMoveFormula(self.position, self.flagList, move, timeOut)
        moveClass = Move.QuanticMove(Move.Move("", self.flags), Move.Move("", self.flags))
        return ChessUtils.evalPosition(self.position, moveClass, self.flagList, timeOut)
    
    def moveHint(self):
        return ChessUtils.moveHint(self.position, self.flagList)