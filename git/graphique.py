import pygame
import sys

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 11  # Number of vertical lines
GRID_HEIGHT = 19  # Number of horizontal lines
MARGIN = 20
BOARD_WIDTH = GRID_SIZE * (GRID_WIDTH - 1)  # Adjust board width to exclude the last line
BOARD_HEIGHT = GRID_SIZE * (GRID_HEIGHT - 1)  # Adjust board height to exclude the last line
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PION_SIZE = 10  # Size of the red dots for valid moves

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

    def draw_board(self, screen):
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.board[i][j] == 1:  # Case noire
                    color = BLACK
                elif self.board[i][j] in ["Q", "@"]:  # Case avec un marqueur
                    color = BLACK
                else:  # Case blanche
                    color = WHITE
                pygame.draw.rect(screen, color, (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE, GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, GREY, (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
        
        
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.board[i][j] == 1 and self.is_valid_move(i, j):
                    self.draw_ring(screen, GREY, (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE), PION_SIZE)

        
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                if self.board[i][j] == "Q":
                    self.draw_ring(screen, RED, (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE), PION_SIZE)
                elif self.board[i][j] == "@":
                    self.draw_ring(screen, BLUE, (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE), PION_SIZE)
                    
    
    def draw_ring(self, screen, color, position, radius):
        pygame.draw.circle(screen, color, position, radius, 2)  

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

class Game:
    def __init__(self):
        self.board = Board()
        self.currentPlayer = "Q"
        self.markersCount = {"Q": 0, "@": 0}
        self.maxMarkers = 5

    def switchPlayer(self):
        self.currentPlayer = "@" if self.currentPlayer == "Q" else "Q"

    def canPlaceMarkers(self):
        return self.markersCount["Q"] < self.maxMarkers or self.markersCount["@"] < self.maxMarkers

    def update_board(self, x, y):
        if self.board.make_move(x, y, self.currentPlayer):
            self.markersCount[self.currentPlayer] += 1
            self.switchPlayer()
    
    def handle_click(self, pos):
        x, y = pos
        col = (x - MARGIN + GRID_SIZE // 2) // GRID_SIZE
        row = (y - MARGIN + GRID_SIZE // 2) // GRID_SIZE
        if 0 <= col < GRID_WIDTH - 1 and 0 <= row < GRID_HEIGHT - 1:  
            if self.canPlaceMarkers():
                self.update_board(row, col)

    def play(self):
        pygame.init()
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Board Game")
        clock = pygame.time.Clock()

        running = True
        while running:
            screen.fill(WHITE)
            self.board.draw_board(screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.canPlaceMarkers():
                        self.handle_click(pygame.mouse.get_pos())

            clock.tick(30)
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.play()
