import pygame, sys
import math
from pygame.locals import QUIT, MOUSEBUTTONDOWN


pygame.init()



# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 11  # Number of vertical lines
GRID_HEIGHT = 19  # Number of horizontal lines
MARGIN = 20
BOARD_WIDTH = GRID_SIZE * (GRID_WIDTH - 1)  # Adjust board width to exclude the last line
BOARD_HEIGHT = GRID_SIZE * (GRID_HEIGHT - 1)  # Adjust board height to exclude the last line
WHITE = (215, 214, 214)
BLACK = (81, 71, 69)
WHITEP = (255, 255, 255)
BLACKP = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PION_SIZE = 15  # Size of the red dots for valid moves

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

    def draw_board(self, screen, selected_marker, ring_count, max_ring):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.board[i][j] == 1:  # Case noire
                    color = BLACKP
                elif self.board[i][j] in ["Q", "@"]:  # Case avec un marqueur
                    color = BLACKP
                
                else:  # Case blanche
                    color = WHITEP
                pygame.draw.rect(screen, color, (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, GREY, (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
        
        
                
        if ring_count["Q"] < max_ring or ring_count["@" ] < max_ring:
            for i in range(GRID_HEIGHT):
                for j in range(GRID_WIDTH):
                    if self.board[i][j] == 1 and self.is_valid_move(i, j):
                        self.prevusiliation(screen, GREY, (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE), PION_SIZE)

        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.board[i][j] == "Q":
                    self.draw_ring(screen, RED, (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE), PION_SIZE)
                elif self.board[i][j] == "@":
                    self.draw_ring(screen, BLUE, (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE), PION_SIZE)
        
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.board[i][j] == "c":  # Marqueur rouge
                    pygame.draw.circle(screen, RED, (MARGIN + j * GRID_SIZE + 5, MARGIN + i * GRID_SIZE + 5), GRID_SIZE // 4)
                elif self.board[i][j] == "o":  # Marqueur bleu
                    pygame.draw.circle(screen, BLUE, (MARGIN + j * GRID_SIZE + 5, MARGIN + i * GRID_SIZE + 5), GRID_SIZE // 4)
            
        if selected_marker:
            self.preview_ring_moves(screen, selected_marker)

    def draw_ring(self, screen, color, position, radius):
        pygame.draw.circle(screen, color, position, radius, 2) 

    def prevusiliation(self, screen, color, position, radius):
        start_angle = 0
        stop_angle = 360
        width = 1
        dash_length = 5

        for i in range(start_angle, stop_angle, dash_length * 2):
            pygame.draw.arc(screen, color, (position[0] - radius, position[1] - radius, radius * 2, radius * 2), math.radians(i), math.radians(i + dash_length), width)

    def preview_ring_moves(self, screen, selected_marker):
        initialRingX, initialRingY = selected_marker
        color = GREY 
        for dx in range(-GRID_WIDTH, GRID_WIDTH):
            for dy in range(-GRID_HEIGHT, GRID_HEIGHT):
                if abs(dx) == abs(dy) and 0 <= initialRingX + dx < GRID_HEIGHT and 0 <= initialRingY + dy < GRID_WIDTH:
                    if self.board[initialRingX + dx][initialRingY + dy] == 1:
                        game = Game()
                        if game.checkRightAfterMarker(initialRingX, initialRingX + dx, initialRingY, initialRingY + dy) and not game.checkIfRingExceeded(initialRingX, initialRingY, initialRingX + dx, initialRingY + dy):
                            self.draw_ring(screen, color, (MARGIN + (initialRingY + dy) * GRID_SIZE, MARGIN + (initialRingX + dx) * GRID_SIZE), PION_SIZE)

    def is_adjacent_to_playable(self, x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_HEIGHT and 0 <= ny < GRID_WIDTH and self.board[nx][ny] == 1:
                return True
        return False

    def is_valid_move(self, x, y):
        if self.board[x][y] != 1:  # Vérifie si la case ciblée a une valeur de 1
            return False
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_HEIGHT and 0 <= ny < GRID_WIDTH and self.board[nx][ny] == 0:
                return True
        return False
    
    def make_move(self, x, y, currentPlayer):
        if self.board[x][y] == 1:  
            self.board[x][y] = currentPlayer
            return True
        return False
    def changeMarker(self, initialRingX, deplacementRingX, initialRingY, deplacementRingY, currentPlayer):
        marker1 = "c"
        marker2 = "o"

        if initialRingX > deplacementRingX and initialRingY > deplacementRingY:
            for x, y in zip(range(initialRingX - 1, deplacementRingX, -1), range(initialRingY - 1, deplacementRingY, -1)):
                if self.board[x][y] == marker2:
                    self.board[x][y] = marker1
                elif self.board[x][y] == marker1:
                    self.board[x][y] = marker2
        elif initialRingX < deplacementRingX and initialRingY > deplacementRingY:
            for x, y in zip(range(initialRingX + 1, deplacementRingX), range(initialRingY - 1, deplacementRingY, -1)):
                if self.board[x][y] == marker2:
                    self.board[x][y] = marker1
                elif self.board[x][y] == marker1:
                    self.board[x][y] = marker2
        elif initialRingX < deplacementRingX and initialRingY < deplacementRingY:
            for x, y in zip(range(initialRingX + 1, deplacementRingX), range(initialRingY + 1, deplacementRingY)):
                if self.board[x][y] == marker2:
                    self.board[x][y] = marker1
                elif self.board[x][y] == marker1:
                    self.board[x][y] = marker2
        elif initialRingX > deplacementRingX and initialRingY < deplacementRingY:
            for x, y in zip(range(initialRingX - 1, deplacementRingX, -1), range(initialRingY + 1, deplacementRingY)):
                if self.board[x][y] == marker2:
                    self.board[x][y] = marker1
                elif self.board[x][y] == marker1:
                    self.board[x][y] = marker2
    
    def checkAligment(self, row, col):
        
        initialValue = self.board[row][col]
        if initialValue == 1:
            return False

        # Vérification horizontale
        count = 1
        for i in range(1, 4):
            if col + i < GRID_WIDTH and self.board[row][col + i] == initialValue:
                count += 1
            else:
                break
        for i in range(1, 4):
            if col - i >= 0 and self.board[row][col - i] == initialValue:
                count += 1
            else:
                break
        if count >= 4:
            return True

        # Vérification verticale
        count = 1
        for i in range(1, 4):
            if row + i < GRID_HEIGHT and self.board[row + i][col] == initialValue:
                count += 1
            else:
                break
        for i in range(1, 4):
            if row - i >= 0 and self.board[row - i][col] == initialValue:
                count += 1
            else:
                break
        if count >= 4:
            return True

        # Vérification diagonale haut-gauche -> bas-droite
        count = 1
        for i in range(1, 4):
            if row + i < GRID_HEIGHT and col + i < GRID_WIDTH and self.board[row + i][col + i] == initialValue:
                count += 1
            else:
                break
        for i in range(1, 4):
            if row - i >= 0 and col - i >= 0 and self.board[row - i][col - i] == initialValue:
                count += 1
            else:
                break
        if count >= 4:
            return True

        # Vérification diagonale bas-gauche -> haut-droite
        count = 1
        for i in range(1, 4):
            if row + i < GRID_HEIGHT and col - i >= 0 and self.board[row + i][col - i] == initialValue:
                count += 1
            else:
                break
        for i in range(1, 4):
            if row - i >= 0 and col + i < GRID_WIDTH and self.board[row - i][col + i] == initialValue:
                count += 1
            else:
                break
        if count >= 4:
            return True

        return False

class Game:
    def __init__(self):
        self.board = Board()
        self.redRing = "Q"
        self.redMarker = "c"
        self.blueRing = "@"
        self.blueMarker = "o"
        self.currentPlayer = "Q"
        self.redNumberAlignment = 0
        self.blueNumberAlignment = 0
        self.ringCount = {"Q": 0, "@": 0}
        self.clock = pygame.time.Clock()
        self.maxRing = 5
        self.state = "placing_markers"  # Other state is "moving_ring"
        self.selected_marker = None

    def switchPlayer(self):
        self.currentPlayer = "@" if self.currentPlayer == "Q" else "Q"

    def canPlaceRings(self):
        return self.ringCount["Q"] < self.maxRing or self.ringCount["@"] < self.maxRing

    def update_board(self, x, y):
        if self.board.make_move(x, y, self.currentPlayer):
            self.ringCount[self.currentPlayer] += 1
            self.switchPlayer()
            
    
    
    def handle_click(self, pos):
        x, y = pos
        col = (x - MARGIN + GRID_SIZE // 2) // GRID_SIZE
        row = (y - MARGIN + GRID_SIZE // 2) // GRID_SIZE
        if 0 <= col < GRID_WIDTH - 1 and 0 <= row < GRID_HEIGHT - 1:  
            if self.state == "placing_markers":
                if self.canPlaceRings():
                    self.update_board(row, col)
                    if self.ringCount["Q"] >= self.maxRing and self.ringCount["@"] >= self.maxRing:
                        self.state = "moving_ring"
            elif self.state == "moving_ring":
                if self.selected_marker:
                    self.move_ring(row, col)
                else:
                    self.select_marker(row, col)
                if self.board.checkAligment(row, col):  # Vérification d'un alignement
                    self.state = "removing_ring"  # Passage à l'état de retrait d'un anneau
            elif self.state == "removing_ring":
                if self.board.board[row][col] == self.currentPlayer:  # Vérification que l'anneau appartient au joueur
                    self.board.board[row][col] = 1  # Retirer l'anneau
                    self.state = "moving_ring"  # Retour à l'état de déplacement d'un anneau
    
    def selectMarkersPlacement(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = (x - MARGIN + GRID_SIZE // 2) // GRID_SIZE
                    row = (y - MARGIN + GRID_SIZE // 2) // GRID_SIZE
                    if 0 <= col < GRID_WIDTH - 1 and 0 <= row < GRID_HEIGHT - 1:
                        if self.currentPlayer == "Q":
                            if self.board.board[row][col] == "Q":
                                self.board.board[row][col] = self.redMarker
                                self.board.draw_board(screen, self.selected_marker)
                                pygame.display.flip()
                                return self.ringPlacement(row, col)
                        else:
                            if self.board.board[row][col] == "@":
                                self.board.board[row][col] = self.blueMarker
                                self.board.draw_board(screen, self.selected_marker)
                                pygame.display.flip()
                                return self.ringPlacement(row, col)
            pygame.display.flip()
            self.clock.tick(30)  # Use self.clock instead of clock
    
    def select_marker(self, row, col):
        if self.board.board[row][col] == self.currentPlayer:
            self.selected_marker = (row, col)
            

    def move_ring(self, row, col):
        initialRingX, initialRingY = self.selected_marker
        if row == initialRingX and col == initialRingY:
            return
        if self.board.board[row][col]!= 1:
            return
        if abs(row - initialRingX)!= abs(col - initialRingY):
            return
        if self.board.board[row][col] in ["Q", "@"]:
            return
        if not self.checkRightAfterMarker(initialRingX, row, initialRingY, col):
            return
        if self.checkIfRingExceeded(initialRingX, initialRingY, row, col):
            return
        self.board.changeMarker(initialRingX, row, initialRingY, col, self.currentPlayer)
        if self.currentPlayer == "Q":
            self.board.board[row][col] = "Q"
            self.board.board[initialRingX][initialRingY] = self.redMarker  # Mettre à jour le marqueur rouge
        else:
            self.board.board[row][col] = "@"
            self.board.board[initialRingX][initialRingY] = self.blueMarker  # Mettre à jour le marqueur bleu
        if self.board.checkAligment(row, col):
            print("Joueur", self.currentPlayer, "a gagné!")
        else:
            self.switchPlayer()
        self.state = "moving_ring"
        self.selected_marker = None
        

    def select_marker(self, row, col):
        if self.board.board[row][col] == self.currentPlayer:
            self.selected_marker = (row, col)
            self.board.board[row][col] = self.currentPlayer + self.redMarker if self.currentPlayer == "Q" else self.currentPlayer + self.blueMarker
    
    def checkRightAfterMarker(self, initialRingX, deplacementRingX, initialRingY, deplacementRingY):
        if initialRingX > deplacementRingX and initialRingY > deplacementRingY:
            isMarkerFound = False
            for x, y in zip(range(initialRingX - 1, deplacementRingX, -1), range(initialRingY - 1, deplacementRingY, -1)):
                if self.board.board[x][y] in {'c', 'o'}:
                    isMarkerFound = True
                if isMarkerFound and self.board.board[x][y] not in {'c', 'o'}:
                    return False
        elif initialRingX < deplacementRingX and initialRingY > deplacementRingY:
            isMarkerFound = False
            for x, y in zip(range(initialRingX + 1, deplacementRingX), range(initialRingY - 1, deplacementRingY, -1)):
                if self.board.board[x][y] in {'c', 'o'}:
                    isMarkerFound = True
                if isMarkerFound and self.board.board[x][y] not in {'c', 'o'}:
                    return False
        elif initialRingX < deplacementRingX and initialRingY < deplacementRingY:
            isMarkerFound = False
            for x, y in zip(range(initialRingX + 1, deplacementRingX), range(initialRingY + 1, deplacementRingY)):
                if self.board.board[x][y] in {'c', 'o'}:
                    isMarkerFound = True
                if isMarkerFound and self.board.board[x][y] not in {'c', 'o'}:
                    return False
        elif initialRingX > deplacementRingX and initialRingY < deplacementRingY:
            isMarkerFound = False
            for x, y in zip(range(initialRingX - 1, deplacementRingX, -1), range(initialRingY + 1, deplacementRingY)):
                if self.board.board[x][y] in {'c', 'o'}:
                    isMarkerFound = True
                if isMarkerFound and self.board.board[x][y] not in {'c', 'o'}:
                    return False
        return True
    
    def checkIfRingExceeded(self, initialRingX, initialRingY, deplacementRingX, deplacementRingY):
        if initialRingX > deplacementRingX and initialRingY > deplacementRingY:
            for x, y in zip(range(initialRingX - 1, deplacementRingX, -1), range(initialRingY - 1, deplacementRingY, -1)):
                if self.board.board[x][y] in {'Q', '@'}:
                    return True
        elif initialRingX < deplacementRingX and initialRingY > deplacementRingY:
            for x, y in zip(range(initialRingX + 1, deplacementRingX), range(initialRingY - 1, deplacementRingY, -1)):
                if self.board.board[x][y] in {'Q', '@'}:
                    return True
        elif initialRingX < deplacementRingX and initialRingY < deplacementRingY:
            for x, y in zip(range(initialRingX + 1, deplacementRingX), range(initialRingY + 1, deplacementRingY)):
                if self.board.board[x][y] in {'Q', '@'}:
                    return True
        elif initialRingX > deplacementRingX and initialRingY < deplacementRingY:
            for x, y in zip(range(initialRingX - 1, deplacementRingX, -1), range(initialRingY + 1, deplacementRingY)):
                if self.board.board[x][y] in {'Q', '@'}:
                    return True
        return False
    
    def ringRemoval(self):
        x = int(input("Saisissez les coordonnées x de l'anneau que vous souhaitez retirer : ")) - 1
        y = int(input("Saisissez les coordonnées y de l'anneau que vous souhaitez retirer : ")) - 1
        if self.board.board[x][y] == self.currentPlayer:
            self.board.board[x][y] = 1
    
    def checkWin(self, initialRingX, deplacementRingX, initialRingY, deplacementRingY):
        if initialRingX > deplacementRingX and initialRingY > deplacementRingY:
            for x, y in zip(range(initialRingX, deplacementRingX, -1), range(initialRingY, deplacementRingY, -1)):
                if self.board.board[x][y] in ['c', 'o']:
                    if self.currentPlayer == "Q":
                        self.redNumberAlignment += 1
                    else:
                        self.blueNumberAlignment += 1
                    return True
        elif initialRingX < deplacementRingX and initialRingY > deplacementRingY:
            for x, y in zip(range(initialRingX, deplacementRingX), range(initialRingY, deplacementRingY, -1)):
                if self.board.board[x][y] in ['c', 'o']:
                    if self.currentPlayer == "Q":
                        self.redNumberAlignment += 1
                    else:
                        self.blueNumberAlignment += 1
                    return True
        elif initialRingY < deplacementRingY and initialRingX > deplacementRingX:
            for x, y in zip(range(initialRingX, deplacementRingX, -1), range(initialRingY, deplacementRingY)):
                if self.board.board[x][y] in ['c', 'o']:
                    if self.currentPlayer == "Q":
                        self.redNumberAlignment += 1
                    else:
                        self.blueNumberAlignment += 1
                    return True
        elif initialRingY < deplacementRingY and initialRingX < deplacementRingX:
            for x, y in zip(range(initialRingX, deplacementRingX), range(initialRingY, deplacementRingY)):
                if self.board.board[x][y] in ['c', 'o']:
                    if self.currentPlayer == "Q":
                        self.redNumberAlignment += 1
                    else:
                        self.blueNumberAlignment += 1
                    return True
        return False
            
    
    
    def play(self):
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Board Game")
        clock = pygame.time.Clock()

        running = True
        while running:
            screen.fill(WHITEP)
            self.board.draw_board(screen, self.selected_marker, self.ringCount, self.maxRing)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())

            clock.tick(30)
        pygame.quit()

# Classe Button pour le menu
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

# Création de la fenêtre
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")
BG = pygame.image.load("assets/yinsh.jpg")

def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def mode_normal():
    game = Game()
    game.play()

def mode_blitz():
    game = Game()
    game.play()

def main_menu():
    pygame.display.set_caption("Menu")
    while True:
        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "blue")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="BLITZ", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="NORMAL", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        SCREEN.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mode_normal()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    mode_blitz()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

main_menu()
