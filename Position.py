import Piece
from utils import ChessUtils
import copy


class Position:

    def __init__(self, listRows, move = None):
        self.listRows = listRows
        if move != None:
            self = self.makeMove(move)

    def isQuantic(self):

        return False
    
    def boardToFen(self, flags):

            fen = ""
            for row in self.listRows:
                rowStr = ""
                emptySpaces = 0
                for piece in row:
                    if (piece is None):
                        emptySpaces += 1
                    else:
                        if emptySpaces > 0:
                            rowStr += str(emptySpaces)
                            emptySpaces = 0
                        rowStr += piece.pieceClass
                if emptySpaces > 0:
                    rowStr += str(emptySpaces)
                fen += rowStr + "/"
            return fen + " " + flags[0] + " " + flags[1] + " " + flags[2] + " 0 1"

    
    def makeMove(self, move):

        if move.isQuantic():
            p0 = Position(copy.deepcopy(self.listRows))
            p1 = Position(copy.deepcopy(self.listRows))
            
            if ChessUtils.isValid(self, move.move0):
                p0.makeMove(move.move0)
            if ChessUtils.isValid(self, move.move1):
                p1.makeMove(move.move1)

            p0.setQuanticWhatOnSquare(move.move0.move[2:4], True)
            p1.setQuanticWhatOnSquare(move.move1.move[2:4], True)
            return QuanticPosition(p0, p1)
        else:
            orCol = ord(move.move[0]) - ord('a')
            orRow = len(self.listRows) - int(move.move[1])
            piece = self.listRows[orRow][orCol]
            if piece.pieceClass in "KkPp" and self.getWhatIsOnSquare(move.move[2:4]) == None:           

                self.listRows = self.complementaryMove(move, piece.pieceClass)
            self.listRows[orRow][orCol] = None
            desCol = ord(move.move[2]) - ord('a')
            desRow = len(self.listRows) - int(move.move[3])
            if piece != None:
                self.listRows[desRow][desCol] = piece
            return AbstractPosition(copy.deepcopy(self))
        
    def noMakeMove(self, move = None):

        return AbstractPosition(copy.deepcopy(self))
        
    def makeQuanticPiece(self, square):

        orCol = ord(square[0]) - ord('a')
        orRow = len(self.listRows) - int(square[1])
        piece = self.listRows[orRow][orCol]
        if piece != None:
            piece.setQuantic(True)
            return piece
        else:
            return None
        
    def setPiece(self, piece, square):

        col = ord(square[0]) - ord('a')
        row = len(self.listRows) - int(square[1])
        self.listRows[row][col] = piece

    def complementaryMove(self, move, piece):

        if piece in "Kk":
            if move.move[0] == "e":
                if move.move[2] == "g":
                    rook = self.listRows[8 - int(move.move[1])][0]
                    self.listRows[8 - int(move.move[1])][7] = None
                    self.listRows[8 - int(move.move[1])][5] = rook
                if move.move[2] == "c":
                    rook = self.listRows[8 - int(move.move[1])][0]
                    self.listRows[8 - int(move.move[1])][0] = None
                    self.listRows[8 - int(move.move[1])][3] = rook
        if (piece in "Pp") and (move.move[0] != move.move[2]):
            if move.flags[2] == move.move[2:4]:
                self.listRows[8 - int(move.move[1])][ord(move.move[2]) - ord('a')] = None
        return self.listRows


    def getWhatIsOnSquare(self, square):

        file = ord(square[0]) - ord('a')
        rank = len(self.listRows) - int(square[1])
        return self.listRows[rank][file]
    
    def setQuanticWhatOnSquare(self, square, quantic):

        piece = self.getWhatIsOnSquare(square)
        if piece !=None:
            piece.setQuantic(quantic)
    
    def deQuantify(self, row, col):

        square = ""
        square += chr(col + ord('a'))
        square += str(row + 1)
        piece = self.getWhatIsOnSquare(square)
        if isinstance(piece, Piece.Piece):
            piece.setQuantic(False)
            return piece
        
    def simpleTree(self):

        return self
        
    def addToAllOnSquare(self, square, index):

        if self.getWhatIsOnSquare(square) is not None:
            self.getWhatIsOnSquare(square).addMoves(index)

    def depth(self):
        return 1

    def __str__(self, level = 0):

        result = "\n+---+---+---+---+---+---+---+---+\n"
        for x in range(len(self.listRows)):
            for y in self.listRows[x]:
                if isinstance(y, (Piece.Piece)):
                    unicodePiece = ChessUtils.get_piece_unicode(y.pieceClass)
                    if y.isQuantic():
                        quant = "|~"
                    else:
                        quant = "| "
                    result += quant + unicodePiece + " "
                else:
                    result += "|   "
            result += "| " + str(8 - x) + "\n+---+---+---+---+---+---+---+---+\n"
        result += "  A   B   C   D   E   F   G   H"
        return result
    
    def strOpt2(self):

        return self.__str__()
    
    def strOpt3(self):
        result = "\n"
        for x in range(len(self.listRows)):
            for y in self.listRows[x]:
                if isinstance(y, (Piece.Piece)):
                    if y.isQuantic():
                        quant = "~"
                    else:
                        quant = " "
                    result += quant + y.pieceClass + "  "
                else:
                    result += " ·  "
            result += "\n\n"
        return result

    
class AbstractPosition(Position):

    def __init__(self, position, move = None):
        self.position = position
        if move != None:
            self = self.makeMove(move)

    def isQuantic(self):

        return self.position.isQuantic()
    
    def boardToFen(self, flags):

        if not self.isQuantic():
            return self.position.boardToFen(flags)
        else:
            raise Exception("You can not have a Quantum Position in FEN notation")
    
    def makeMove(self, move):

        return AbstractPosition(copy.deepcopy(self.position.makeMove(move)))
    
    def noMakeMove(self, move = None):

        self.position = self.position.noMakeMove(move)
        return self
    
    def makeQuanticPiece(self, square):
        return self.position.makeQuanticPiece(square)
    
    def setPiece(self, piece, square):

        self.position.setPiece(piece, square)
    
    def getWhatIsOnSquare(self, square):

        return self.position.getWhatIsOnSquare(square)
    
    def setQuanticWhatOnSquare(self, square, quantic):

        self.position.setQuanticWhatOnSquare(square, quantic)
    
    def mergePosition(self, move, choice):

        if move == 0:
            return self
        else:
            return AbstractPosition(copy.deepcopy(self.position).mergePosition(move - 1, choice))
        
    def deQuantify(self, row, col):        

        return self.position.deQuantify(row, col)
    
    def simpleTree(self):

        return self.position.simpleTree()
        
    def addToAllOnSquare(self, square, index):

        self.position.addToAllOnSquare(square, index)

    def depth(self):
        return self.position.depth() + 1

    def __str__(self, level=0):

        return self.position.__str__(level)
    
    def strOpt2(self):

        return self.position.strOpt2()
        
    def strOpt3(self):

        return self.position.strOpt3()
    
class QuanticPosition(Position):

    def __init__(self, position0, position1, move = None):
        self.position0 = position0
        self.position1 = position1
        if move != None:
            self = self.makeMove(move)            

    def isQuantic(self):

        return True
    
    def boardToFen(self, flags):
        raise Exception("Quantic positions can not be converted to FEN")
    
    def setPosition(self, position):

        if position.isQuantic() and self.isQuantic():
            self.position0 = copy.deepcopy(position.position0.simpleTree())
            self.position1 = copy.deepcopy(position.position1.simpleTree()) 
        else:
            self.listRows = copy.deepcopy(position.listRows)

    def makeMove(self, move):

        validForPos0 = move.isValid(self.position0)
        validForPos1 = move.isValid(self.position1)
        QEntanglement = []
        key0 = 1
        key1 = 1
        if move.isQuantic():
            moveStr = move.move0.move
            if validForPos0 and not validForPos1:
                if move.move0.isValid(self.position1):
                    moveStr = move.move1.move
            if validForPos1 and not validForPos0:
                if move.move0.isValid(self.position0):
                    moveStr = move.move1.move
        else:
            moveStr = move.move
        if validForPos0 and not validForPos1:
            QEntanglement = ChessUtils.getInterference(self.position1, moveStr)
            self.position1 = self.position1.noMakeMove(move) 
            key1 = 0
        elif validForPos1 and not validForPos0:
            QEntanglement = ChessUtils.getInterference(self.position0, moveStr)
            self.position0 = self.position0.noMakeMove(move) 
            key0 = 0
        piece = self.getWhatIsOnSquare(moveStr[0:2])
        if piece:
            piece.addMoves(QEntanglement)
        if validForPos0 or (move.isQuantic() and key0):
            self.position0 = self.position0.makeMove(move)
        if validForPos1 or (move.isQuantic() and key1):
            self.position1 = self.position1.makeMove(move)
        return self
    
    def noMakeMove(self, move = None):

        self.position0 = self.position0.noMakeMove(move)
        self.position1 = self.position1.noMakeMove(move)
        return self
    
    def setPiece(self, piece, square):

        self.position0.setPiece(piece, square)
        self.position1.setPiece(piece, square)
    
    def getWhatIsOnSquare(self, square):

        p0 = self.position0.getWhatIsOnSquare(square)
        p1 = self.position1.getWhatIsOnSquare(square)
        if p0 == None:
            return p1
        else:
            return p0
                    
    def setQuanticWhatOnSquare(self, square, quantic):

        self.position0.setQuanticWhatOnSquare(square, quantic)
        self.position1.setQuanticWhatOnSquare(square, quantic)
            
    def mergePosition(self, move, choice):

        if move == 0:
            listPos = [self.position0, self.position1]
            return AbstractPosition(listPos[choice])
        else:
            return QuanticPosition(copy.deepcopy(self.position0.mergePosition(move - 1, choice)), copy.deepcopy(self.position1.mergePosition(move - 1, choice)))

    def deQuantify(self, row, col):

        square = ""
        square += chr(col + ord('a'))
        square += str(row + 1)
        piece = self.getWhatIsOnSquare(square)
        listMoves = []
        if isinstance(piece, Piece.Piece):
            listMoves = copy.deepcopy(piece.listMoves)
        deqPos0 = self.position0.deQuantify(row, col)
        deqPos1 = self.position1.deQuantify(row, col)
        if isinstance(deqPos0, Piece.Piece):
            if isinstance(deqPos1, Piece.Piece):
                if deqPos0.pieceClass == deqPos1.pieceClass and (not deqPos0.isQuantic()) and (not deqPos1.isQuantic()):
                    return deqPos0
                else:
                    deqPos0 = deqPos0.setQuantic(True)
                    deqPos0.addMoves(listMoves)
                    return deqPos0
            else:
                deqPos0 = deqPos0.setQuantic(True)
                deqPos0.addMoves(listMoves)
                return deqPos0
        elif isinstance(deqPos1, Piece.Piece):
            deqPos1 = deqPos1.setQuantic(True)
            deqPos1.addMoves(listMoves)
            return deqPos1
        else:
            return None
        
    def simpleTree(self):

        return QuanticPosition(copy.deepcopy(self.position0.simpleTree()), copy.deepcopy(self.position1.simpleTree()))
    
    def addToAllOnSquare(self, square, index):

        self.position0.addToAllOnSquare(square, index)
        self.position1.addToAllOnSquare(square, index)
        
    def depth(self):
        d0 = self.position0.depth() + 1
        d1 = self.position1.depth() + 1
        if d0 == d1:
            return d0
        else:
            raise Exception("error, levels differ: " + str(d0) + ", " + str(d1))

    def __str__(self, level = 1):

        return "Quantic position:\n" + ("\t" * level) +"Position 1: " + self.position0.__str__(level + 1) + "\n" + ("\t" * level) +"Position 2: " + self.position1.__str__(level + 1) + "\n"
    
    def strOpt2(self):

        result = "+---+---+---+---+---+---+---+---+\n"
        for x in range(8):
            for y in range(8):
                col = str(chr(y + ord('a')))
                row = str(8 - x)
                piece = self.getWhatIsOnSquare(col + row)
                if isinstance(piece, (Piece.Piece)):
                    unicodePiece = ChessUtils.get_piece_unicode(piece.pieceClass)
                    if piece.isQuantic():
                        quant = "|~"
                    else:
                        quant = "| "
                    result += quant + unicodePiece + " "
                else:
                    result += "|   "
            result += "| " + str(8 - x) + "\n+---+---+---+---+---+---+---+---+\n"
        result += "  A   B   C   D   E   F   G   H"
        return "\n" + result
    
    def strOpt3(self):

        result = "\n"
        for x in range(8):
            for y in range(8):
                col = str(chr(y + ord('a')))
                row = str(8 - x)
                piece = self.getWhatIsOnSquare(col + row)
                if isinstance(piece, (Piece.Piece)):
                    if piece.isQuantic():
                        quant = "~"
                    else:
                        quant = " "
                    result += quant + piece.pieceClass + " "
                else:
                    result += " · "
            result +="\n\n"
        return result
    