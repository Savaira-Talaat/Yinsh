class Board:
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

    def displayBoard(self):
        for i in range(len(self.board)):
            print(i + 1, end='    ')
            for j in range(len(self.board[0])):
                if self.board[i][j] == 1:
                    print('* ', end='')
                elif self.board [i][j] == "Q" or self.board[i][j] == 'c' or self.board[i][j] == '@' or self.board[i][j] == 'o':
                    print(f'{self.board[i][j]} ', end='')
                else:
                    print('  ', end='')
            print()

        print('      ', end='')
        for j in range(len(self.board[0])):
            print(f'{j + 1} ', end='')
        print()
        
    def is_valid_move(self, x, y):
        return 0 <= x < len(self.board) and 0 <= y < len(self.board[0]) and self.board[x][y] == 1

    def make_move(self, x, y, currentPlayer):
        if self.is_valid_move(x, y):
            self.board[x][y] = currentPlayer
            return True
        return False
        
class Game:
    def __init__(self):
        self.board = Board()
        self.currentPlayer = "Q"
        self.blackRing = "Q"
        self.blackMarker = "c"
        self.whiteRing = "@"
        self.whiteMarker = "o"
        self.ringCount = {"Q" : 0, "@" : 0}
        self.maxRings = 5
                
    def switchPlayer(self):
        if self.currentPlayer == "Q":
            self.currentPlayer = "@"
        else:
            self.currentPlayer = "Q"
    
    def canPlaceRings(self):
        return self.ringCount["Q"] < self.maxRings or self.ringCount["@"] < self.maxRings
            
    def play(self):
        while self.canPlaceRings():
            self.board.displayBoard()
            if self.ringCount[self.currentPlayer] < self.maxRings:
                print(f"C'est au tour du joueur {self.currentPlayer}")
                try:
                    x = int(input("Saisissez les coordonnées x de la case où vous souhaitez vous rendre : ")) - 1
                    y = int(input("Saisissez les coordonnées y de la case où vous souhaitez vous rendre : ")) - 1
                except ValueError:
                    print("Veuillez entrer des nombres valides.")
                    continue
            
                if self.board.make_move(x, y, self.currentPlayer):
                    self.ringCount[self.currentPlayer] += 1
                    self.switchPlayer()
                else:
                    print("Coordonnées invalides ou case non disponible. Veuillez réessayer.")
            else:
                print(f"Le joueur {self.currentPlayer} a déjà placé ses anneaux")
                self.switchPlayer()
                
        print("Tous les anneaux ont été placés, la partie peut commencer")
        self.board.displayBoard()
        
if __name__ == "__main__":
    game = Game()
    game.play()
    