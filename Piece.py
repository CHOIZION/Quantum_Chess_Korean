class Piece:
    def __init__(self, pieceClass):
        self.pieceClass = pieceClass
        self.quantic = False
        self.listMoves = []

    def setQuantic(self, quantic):

        self.quantic = quantic
        if not quantic:
            self.listMoves.clear()
        return self
        
    def addMoves(self, moves = []):

        union = list(set(moves) | set(self.listMoves))
        self.listMoves = union
        return self.listMoves

    def isQuantic(self):

        return self.quantic
