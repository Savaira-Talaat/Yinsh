import pygame, sys
from pygame.locals import QUIT, MOUSEBUTTONDOWN

pygame.init()

# Paramètres du jeu de plateau
GRID_SIZE = 40
MARGIN = 5
GRID_WIDTH = 11
GRID_HEIGHT = 19
WINDOW_WIDTH = GRID_WIDTH * GRID_SIZE + (GRID_WIDTH + 1) * MARGIN
WINDOW_HEIGHT = GRID_HEIGHT * GRID_SIZE + (GRID_HEIGHT + 1) * MARGIN
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Classe Board
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

    def is_adjacent_to_playable(self, x, y):
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_HEIGHT and 0 <= ny < GRID_WIDTH and self.board[nx][ny] == 1:
                return True
        return False

    def draw_board(self, screen):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                color = BLACK if self.board[i][j] == 1 else WHITE
                pygame.draw.rect(screen, color, (MARGIN + j * GRID_SIZE + 1, MARGIN + i * GRID_SIZE + 1, GRID_SIZE - 2, GRID_SIZE - 2))
                if self.board[i][j] == 1:
                    pygame.draw.rect(screen, GREY, (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                if self.board[i][j] == 0 and self.is_adjacent_to_playable(i, j):
                    pygame.draw.rect(screen, GREY, (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                if self.board[i][j] == "Q":
                    pygame.draw.circle(screen, RED, (MARGIN + j * GRID_SIZE + GRID_SIZE // 2, MARGIN + i * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 5)
                elif self.board[i][j] == "@":
                    pygame.draw.circle(screen, BLUE, (MARGIN + j * GRID_SIZE + GRID_SIZE // 2, MARGIN + i * GRID_SIZE + GRID_SIZE // 2), GRID_SIZE // 2 - 5)

    def is_valid_move(self, x, y):
        return 0 <= x < GRID_HEIGHT and 0 <= y < GRID_WIDTH and self.board[x][y] == 1

    def make_move(self, x, y, currentPlayer):
        if self.is_valid_move(x, y):
            self.board[x][y] = currentPlayer
            return True
        return False

    def check_win(self, player):
        def check_direction(x, y, dx, dy):
            count = 0
            nx, ny = x, y
            while 0 <= nx < GRID_HEIGHT and 0 <= ny < GRID_WIDTH:
                if self.board[nx][ny] == player:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
                nx += dx
                ny += dy
            return False

        for x in range(GRID_HEIGHT):
            for y in range(GRID_WIDTH):
                if self.board[x][y] == player:
                    if (check_direction(x, y, 1, 0) or  # Horizontal
                        check_direction(x, y, 0, 1) or  # Vertical
                        check_direction(x, y, 1, 1) or  # Diagonal /
                        check_direction(x, y, 1, -1)):  # Diagonal \
                        return True
        return False

# Classe Game
class Game:
    def __init__(self):
        self.board = Board()
        self.currentPlayer = "Q"
        self.markersCount = {"Q": 0, "@": 0}
        self.maxMarkers = 5
        self.winner = None

    def switchPlayer(self):
        self.currentPlayer = "@" if self.currentPlayer == "Q" else "Q"

    def canPlaceMarkers(self):
        return self.markersCount["Q"] < self.maxMarkers or self.markersCount["@"] < self.maxMarkers

    def handle_click(self, pos):
        x, y = pos
        row = (y - MARGIN) // GRID_SIZE
        col = (x - MARGIN) // GRID_SIZE
        if 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH:
            if self.board.make_move(row, col, self.currentPlayer):
                self.markersCount[self.currentPlayer] += 1
                if self.board.check_win(self.currentPlayer):
                    self.winner = self.currentPlayer
                self.switchPlayer()

    def play(self):
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Board Game")
        clock = pygame.time.Clock()

        running = True
        while running:
            screen.fill(WHITE)
            self.board.draw_board(screen)
            if self.winner:
                font = pygame.font.SysFont(None, 74)
                text = font.render(f"Player {self.winner} wins!", True, BLACK)
                screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.winner:
                    if self.canPlaceMarkers():
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
    pygame.display.set_caption("Blitz")
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")
        OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        OPTIONS_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
        pygame.display.update()

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
