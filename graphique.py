import pygame
import sys

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 30
GRID_WIDTH = 11
GRID_HEIGHT = 19
MARGIN = 20
BOARD_WIDTH = GRID_SIZE * GRID_WIDTH
BOARD_HEIGHT = GRID_SIZE * GRID_HEIGHT
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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
    def displayBoard(self, canvas):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                x1, y1 = self.get_position(i, j, 30)
                x2, y2 = self.get_position(i, j, 50)
                canvas.create_rectangle(x1, y1, x2, y2, outline="gray", width=2)
                if self.board[i][j] == 1:
                    canvas.create_rectangle(x1, y1, x2, y2, outline="white", width=2)
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
                    pygame.draw.rect(screen, GREY, (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)  # Dessiner un contour gris autour des cases remplies
                if self.board[i][j] == 0 and self.is_adjacent_to_playable(i, j):
                    pygame.draw.rect(screen, GREY, (MARGIN + j * GRID_SIZE, MARGIN + i * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)  # Dessiner un contour gris autour des cases vides adjacentes à une case jouable
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

    def handle_click(self, pos):
        x, y = pos
        row = (x - MARGIN) // GRID_SIZE
        col = (y - MARGIN) // GRID_SIZE
        if 0 <= row < GRID_HEIGHT and 0 <= col < GRID_WIDTH:
            if self.board.make_move(col, row, self.currentPlayer):
                self.markersCount[self.currentPlayer] += 1
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
