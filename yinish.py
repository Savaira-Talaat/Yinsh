class Game:
    def __init__(self):
        self.board = [
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0],
            [0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0]
        ]

        self.redRing = "Q"
        self.redMarker = "c"
        self.blueRing = "@"
        self.blueMarker = "o"
        self.currentPlayer = "Q"
        self.redNumberAlignment = 0
        self.blueNumberAlignment = 0
        self.ringCount = {"Q": 0, "@": 0}
        self.maxRing = 5

    def displayBoard(self):
        for i in range(len(self.board)):
            print(i + 1, end='    ')
            for j in range(len(self.board[0])):
                if self.board[i][j] == 1:
                    print('* ', end='')
                elif self.board[i][j] in {'Q', 'c', '@', 'o'}:
                    print(f'{self.board[i][j]} ', end='')
                else:
                    print('  ', end='')
            print()

        print('      ', end='')
        for j in range(len(self.board[0])):
            print(f'{j + 1} ', end='')
        print()

    def selectMove(self):
        while True:
            x = int(input("Saisissez les coordonnées x de la case où vous souhaitez placer votre anneau : ")) - 1
            y = int(input("Saisissez les coordonnées y de la case où vous souhaitez placer votre anneau : ")) - 1

            if 0 <= x < len(self.board) and 0 <= y < len(self.board[0]) and self.board[x][y] == 1:
                self.board[x][y] = self.currentPlayer
                return
            else:
                print("Coordonnées invalides. Veuillez réessayer.")

    def switchPlayer(self):
        self.currentPlayer = "@" if self.currentPlayer == "Q" else "Q"

    def canPlaceRings(self):
        return self.ringCount[self.redRing] < self.maxRing or self.ringCount[self.blueRing] < self.maxRing

    def selectMarkersPlacement(self):
        while True:
            initialRingX = int(input("Saisissez les coordonnées x de la case où vous souhaitez vous placer : ")) - 1
            initialRingY = int(input("Saisissez les coordonnées y de la case où vous souhaitez vous placer : ")) - 1
            if self.currentPlayer == "Q":
                if 0 <= initialRingX < len(self.board) and 0 <= initialRingY < len(self.board[0]) and self.board[initialRingX][initialRingY] == "Q":
                    self.board[initialRingX][initialRingY] = self.redMarker
                    self.displayBoard()
                    return self.ringPlacement(initialRingX, initialRingY)
                else:
                    print("Coordonnées invalides. Veuillez réessayer.")
            else:
                if 0 <= initialRingX < len(self.board) and 0 <= initialRingY < len(self.board[0]) and self.board[initialRingX][initialRingY] == "@":
                    self.board[initialRingX][initialRingY] = self.blueMarker
                    self.displayBoard()
                    return self.ringPlacement(initialRingX, initialRingY)
                else:
                    print("Coordonnées invalides. Veuillez réessayer.")
            self.displayBoard()

    def ringPlacement(self, initialRingX, initialRingY):
        print("Déplacement de l'anneau")
        incorrectPosition = True
        while incorrectPosition:
            deplacementRingX = int(input("Saisissez les coordonnées x de la case où vous souhaitez vous rendre : ")) - 1
            deplacementRingY = int(input("Saisissez les coordonnées y de la case où vous souhaitez vous rendre : ")) - 1
            if deplacementRingX == initialRingX and deplacementRingY == initialRingY:
                print("Vous avez saisis les mêmes coordonnées que celle de la case du marqueur où vous vous êtes placés")
                continue
            elif self.board[deplacementRingX][deplacementRingY] != 1:
                print("Ce n'est pas un déplacement en interligne.")
                continue
            elif abs(deplacementRingX - initialRingX) != abs(deplacementRingY - initialRingY):
                print("Ce n'est pas une direction possible.")
                continue
            elif self.board[deplacementRingX][deplacementRingY] in {"Q", "@"}:
                print("Un anneau est déjà dans cette case.")
                continue
            elif self.checkIfRingExceeded(initialRingX, initialRingY, deplacementRingX, deplacementRingY):
                print("Vous avez dépassé un anneau.")
                continue
            if not self.checkRightAfterMarker(initialRingX, deplacementRingX, initialRingY, deplacementRingY):
                print("Vous ne vous êtes pas arrêtés juste après un marqueur")
                continue
            if self.currentPlayer == "Q":
                self.board[deplacementRingX][deplacementRingY] = self.redRing
            else:
                self.board[deplacementRingX][deplacementRingY] = self.blueRing
            incorrectPosition = False
            self.changeMarker(initialRingX, deplacementRingX, initialRingY, deplacementRingY)
            return self.checkWin(initialRingX, deplacementRingX, initialRingY, deplacementRingY)
        return False

    def checkRightAfterMarker(self, initialRingX, deplacementRingX, initialRingY, deplacementRingY):
        if initialRingX > deplacementRingX and initialRingY > deplacementRingY:
            isMarkerFound = False
            for x, y in zip(range(initialRingX - 1, deplacementRingX, -1), range(initialRingY - 1, deplacementRingY, -1)):
                if self.board[x][y] in {'c', 'o'}:
                    isMarkerFound = True
                if isMarkerFound and self.board[x][y] not in {'c', 'o'}:
                    return False
        elif initialRingX < deplacementRingX and initialRingY > deplacementRingY:
            isMarkerFound = False
            for x, y in zip(range(initialRingX + 1, deplacementRingX), range(initialRingY - 1, deplacementRingY, -1)):
                if self.board[x][y] in {'c', 'o'}:
                    isMarkerFound = True
                if isMarkerFound and self.board[x][y] not in {'c', 'o'}:
                    return False
        elif initialRingX < deplacementRingX and initialRingY < deplacementRingY:
            isMarkerFound = False
            for x, y in zip(range(initialRingX + 1, deplacementRingX), range(initialRingY + 1, deplacementRingY)):
                if self.board[x][y] in {'c', 'o'}:
                    isMarkerFound = True
                if isMarkerFound and self.board[x][y] not in {'c', 'o'}:
                    return False
        elif initialRingX > deplacementRingX and initialRingY < deplacementRingY:
            isMarkerFound = False
            for x, y in zip(range(initialRingX - 1, deplacementRingX, -1), range(initialRingY + 1, deplacementRingY)):
                if self.board[x][y] in {'c', 'o'}:
                    isMarkerFound = True
                if isMarkerFound and self.board[x][y] not in {'c', 'o'}:
                    return False
        return True

    def checkIfRingExceeded(self, initialRingX, initialRingY, deplacementRingX, deplacementRingY):
        if initialRingX > deplacementRingX and initialRingY > deplacementRingY:
            for x, y in zip(range(initialRingX - 1, deplacementRingX, -1), range(initialRingY - 1, deplacementRingY, -1)):
                if self.board[x][y] in {'Q', '@'}:
                    return True
        elif initialRingX < deplacementRingX and initialRingY > deplacementRingY:
            for x, y in zip(range(initialRingX + 1, deplacementRingX), range(initialRingY - 1, deplacementRingY, -1)):
                if self.board[x][y] in {'Q', '@'}:
                    return True
        elif initialRingX < deplacementRingX and initialRingY < deplacementRingY:
            for x, y in zip(range(initialRingX + 1, deplacementRingX), range(initialRingY + 1, deplacementRingY)):
                if self.board[x][y] in {'Q', '@'}:
                    return True
        elif initialRingX > deplacementRingX and initialRingY < deplacementRingY:
            for x, y in zip(range(initialRingX - 1, deplacementRingX, -1), range(initialRingY + 1, deplacementRingY)):
                if self.board[x][y] in {'Q', '@'}:
                    return True
        return False

    def changeMarker(self, initialRingX, deplacementRingX, initialRingY, deplacementRingY):
        if self.currentPlayer == "Q":
            marker1 = "c"
            marker2 = "o"
        else:
            marker1 = "o"
            marker2 = "c"

        if initialRingX > deplacementRingX and initialRingY > deplacementRingY:
            for x, y in zip(range(initialRingX - 1, deplacementRingX, -1), range(initialRingY - 1, deplacementRingY, -1)):
                if self.board[x][y] == marker2:
                    self.board[x][y] = marker1
        elif initialRingX < deplacementRingX and initialRingY > deplacementRingY:
            for x, y in zip(range(initialRingX + 1, deplacementRingX), range(initialRingY - 1, deplacementRingY, -1)):
                if self.board[x][y] == marker2:
                    self.board[x][y] = marker1
        elif initialRingX < deplacementRingX and initialRingY < deplacementRingY:
            for x, y in zip(range(initialRingX + 1, deplacementRingX), range(initialRingY + 1, deplacementRingY)):
                if self.board[x][y] == marker2:
                    self.board[x][y] = marker1
        elif initialRingX > deplacementRingX and initialRingY < deplacementRingY:
            for x, y in zip(range(initialRingX - 1, deplacementRingX, -1), range(initialRingY + 1, deplacementRingY)):
                if self.board[x][y] == marker2:
                    self.board[x][y] = marker1

    def checkWin(self, initialRingX, deplacementRingX, initialRingY, deplacementRingY):
        if initialRingX > deplacementRingX and initialRingY > deplacementRingY:
            for x, y in zip(range(initialRingX, deplacementRingX, -1), range(initialRingY, deplacementRingY, -1)):
                if self.checkAligment(x, y):
                    if self.currentPlayer == "Q":
                        self.redNumberAlignment += 1
                    else:
                        self.blueNumberAlignment += 1
                    return True
        elif initialRingX < deplacementRingX and initialRingY > deplacementRingY:
            for x, y in zip(range(initialRingX, deplacementRingX), range(initialRingY, deplacementRingY, -1)):
                if self.checkAligment(x, y):
                    if self.currentPlayer == "Q":
                        self.redNumberAlignment += 1
                    else:
                        self.blueNumberAlignment += 1
                    return True
        elif initialRingY < deplacementRingY and initialRingX > deplacementRingX:
            for x, y in zip(range(initialRingX, deplacementRingX, -1), range(initialRingY, deplacementRingY)):
                if self.checkAligment(x, y):
                    if self.currentPlayer == "Q":
                        self.redNumberAlignment += 1
                    else:
                        self.blueNumberAlignment += 1
                    return True
        elif initialRingY < deplacementRingY and initialRingX < deplacementRingX:
            for x, y in zip(range(initialRingX, deplacementRingX), range(initialRingY, deplacementRingY)):
                if self.checkAligment(x, y):
                    if self.currentPlayer == "Q":
                        self.redNumberAlignment += 1
                    else:
                        self.blueNumberAlignment += 1
                    return True
        return False

    def checkAligment(self, x, y):
        initialValue = self.board[x][y]
        alignment = 0
        indices = []
        for i, j in zip(range(x, x + 5), range(y, y + 5)):
            if self.board[i][j] == initialValue and self.board[i][j] != 1:
                alignment += 1
                indices.append((i, j))
        if alignment >= 5:
            for i, j in indices:
                if 0 <= i < len(self.board) and 0 <= j < len(self.board[i]):
                    self.board[i][j] = 1
            return True

        initialValue = self.board[x][y]
        alignment = 0
        indices = []
        for i, j in zip(range(x, x + 5), range(y, y - 5, -1)):
            if self.board[i][j] == initialValue and self.board[i][j] != 1:
                alignment += 1
                indices.append((i, j))
        if alignment >= 5:
            for i, j in indices:
                if 0 <= i < len(self.board) and 0 <= j < len(self.board[i]):
                    self.board[i][j] = 1
            return True

        initialValue = self.board[x][y]
        alignment = 0
        indices = []
        for i, j in zip(range(x, x - 5, -1), range(y, y + 5)):
            if self.board[i][j] == initialValue and self.board[i][j] != 1:
                alignment += 1
                indices.append((i, j))
        if alignment >= 5:
            for i, j in indices:
                if 0 <= i < len(self.board) and 0 <= j < len(self.board[i]):
                    self.board[i][j] = 1
            return True

        initialValue = self.board[x][y]
        alignment = 0
        indices = []
        for i, j in zip(range(x, x - 5, -1), range(y, y - 5, -1)):
            if self.board[i][j] == initialValue and self.board[i][j] != 1:
                alignment += 1
                indices.append((i, j))
        if alignment >= 5:
            for i, j in indices:
                if 0 <= i < len(self.board) and 0 <= j < len(self.board[i]):
                    self.board[i][j] = 1
            return True
        return False

    def ringRemoval(self):
        x = int(input("Saisissez les coordonnées x de l'anneau que vous souhaitez retirer : ")) - 1
        y = int(input("Saisissez les coordonnées y de l'anneau que vous souhaitez retirer : ")) - 1
        if (self.currentPlayer == "Q" and self.board[x][y] == "Q") or (self.currentPlayer == "@" and self.board[x][y] == "@"):
            self.board[x][y] = 1

    def mainGameLoop(self, numberAlignmentToWin):
        while self.canPlaceRings():
            self.displayBoard()
            if self.ringCount[self.currentPlayer] < self.maxRing:
                print(f"C'est au tour du joueur {self.currentPlayer}")
                self.selectMove()
                self.ringCount[self.currentPlayer] += 1
            else:
                print(f"Le joueur {self.currentPlayer} a déjà placé ses {self.maxRing}")
            self.switchPlayer()
        print("Tous les marqueurs ont été placés, débutons la partie.")
        self.displayBoard()

        while True:
            self.displayBoard()
            print(f"C'est au tour du joueur {self.currentPlayer} de placer un marqueur.")
            win = self.selectMarkersPlacement()
            if win:
                self.displayBoard()
                print(f"Premier alignement fait par le joueur: {self.currentPlayer}, nombre d'alignements faits par le joueur rouge : {self.redNumberAlignment} et nombre d'alignements faits par le joueur bleu : {self.blueNumberAlignment}")
                if self.redNumberAlignment == numberAlignmentToWin:
                    print(f"Félicitations, le joueur {self.currentPlayer} a gagné")
                    break
                elif self.blueNumberAlignment == numberAlignmentToWin:
                    print(f"Félicitations, le joueur {self.currentPlayer} a gagné")
                    break
                self.ringRemoval()
            self.switchPlayer()


game = Game()
game.mainGameLoop(3)
