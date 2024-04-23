import pygame
import random
import sys

# COLOR
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GOLD = (255, 215, 0)
FONT_COLOR = WHITE
OVERLAY_COLOR = (0, 0, 0, 128)  # Black color with transparency

# Initialize pygame
pygame.init()

# Set up the display
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
GRID_SIZE = 9
CELL_SIZE = SCREEN_WIDTH // GRID_SIZE
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sudoku by Zuzanna Szyber & Wiktoria Polus")

# Load the board image
landescape = pygame.image.load("landescape.jpg")
landescape = pygame.transform.scale(landescape, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Scale the image to fit the window

# Define the Sudoku board
def create_board(difficulty=20):
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    solve_sudoku(board)
    
    # Remove cells to create a puzzle
    cells_to_remove = 81 - difficulty
    while cells_to_remove > 0:
        row, col = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if board[row][col] != 0:
            board[row][col] = 0
            cells_to_remove -= 1

    return board

# Save defined sudoku puzzle
def save_index(board):
    list = []
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            if board[x][y] != 0:
                temp = (x,y)
                list.append(temp)
    print(list)
    return list

def print_board(board):
    for row in board:
        print(row)

def is_valid_move(board, row, col, num):
    # Check if the number is already in the row or column
    
    for i in range(GRID_SIZE):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check if the number is already in the 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
            
    return True

def solve_sudoku(board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                for num in range(1, GRID_SIZE + 1):
                    if is_valid_move(board, row, col, num):
                        board[row][col] = num
                        if solve_sudoku(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def is_board_solved(board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 0:
                return False
    return True

def draw_board(board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            cell_value = board[row][col]
            if cell_value != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(cell_value), True, FONT_COLOR)
                text_rect = text.get_rect(center=(col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2))
                SCREEN.blit(text, text_rect)
            else:
                draw_overlay(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)   # Apply the overlay to empty cells 
        
def draw_cursor(x, y):
    pygame.draw.rect(SCREEN, BLACK, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)

def display_winner_message():
    font = pygame.font.Font(None, 72)
    text = font.render("WINNER!!!", True, GOLD)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    SCREEN.blit(text, text_rect)

def draw_overlay(x, y, width, height):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill(OVERLAY_COLOR)
    SCREEN.blit(overlay, (x, y))

def draw_grid():
    for i in range(1, GRID_SIZE):
        if i % 3 == 0:
            pygame.draw.line(SCREEN, WHITE, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT), 3)
            pygame.draw.line(SCREEN, WHITE, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), 3)
        else:
            pygame.draw.line(SCREEN, WHITE, (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT), 1)
            pygame.draw.line(SCREEN, WHITE, (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE), 1)

def main():
    game_board = create_board(30)  # Adjust difficulty here
    listOfIndexes = save_index(game_board)
    print_board(game_board)

    selected_cell = None
    winner = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not winner:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    x //= CELL_SIZE
                    y //= CELL_SIZE
                    selected_cell = (x, y)
                if event.type == pygame.KEYDOWN:
                    if selected_cell:
                        x, y = selected_cell
                        if event.key in range(pygame.K_1, pygame.K_9 + 1):
                            num = event.key - pygame.K_0
                            if is_valid_move(game_board, y, x, num):
                                if (y, x) not in listOfIndexes:
                                    game_board[y][x] = num
                                if is_board_solved(game_board):
                                    winner = True
                    if event.key == pygame.K_c:  # Clear the selected cell
                        x, y = selected_cell
                        if (y, x) not in listOfIndexes:
                            game_board[y][x] = 0

        SCREEN.blit(landescape, (0, 0))

        draw_grid()  # Draw white frames to simulate a Sudoku board

        draw_board(game_board)
        if selected_cell:
            draw_cursor(*selected_cell)

        if winner:
            display_winner_message()

        pygame.display.flip()

if __name__ == "__main__":
    main()
