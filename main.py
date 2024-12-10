import pygame
import random

# Pygame 초기화
pygame.font.init()

# --- 상수 정의 ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30
PLAY_WIDTH = GRID_WIDTH * BLOCK_SIZE  # 300 px
PLAY_HEIGHT = GRID_HEIGHT * BLOCK_SIZE  # 600 px
TOP_LEFT_X = (WINDOW_WIDTH - PLAY_WIDTH) // 2
TOP_LEFT_Y = WINDOW_HEIGHT - PLAY_HEIGHT

# 색상 정의
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 테트로미노 정의
SHAPE_FORMATS = {
    "S": [['.....',
           '.....',
           '..00.',
           '.00..',
           '.....'],
          ['.....',
           '..0..',
           '..00.',
           '...0.',
           '.....']],
    "Z": [['.....',
           '.....',
           '.00..',
           '..00.',
           '.....'],
          ['.....',
           '..0..',
           '.00..',
           '.0...',
           '.....']],
    "I": [['..0..',
           '..0..',
           '..0..',
           '..0..',
           '.....'],
          ['.....',
           '0000.',
           '.....',
           '.....',
           '.....']],
    "O": [['.....',
           '.....',
           '.00..',
           '.00..',
           '.....']],
    "J": [['.....',
           '.0...',
           '.000.',
           '.....',
           '.....'],
          ['.....',
           '..00.',
           '..0..',
           '..0..',
           '.....']],
    "L": [['.....',
           '...0.',
           '.000.',
           '.....',
           '.....'],
          ['.....',
           '..0..',
           '..0..',
           '..00.',
           '.....']],
    "T": [['.....',
           '..0..',
           '.000.',
           '.....',
           '.....'],
          ['.....',
           '..0..',
           '..00.',
           '..0..',
           '.....']]
}

SHAPE_COLORS = {
    "S": (0, 255, 0),
    "Z": (255, 0, 0),
    "I": (0, 255, 255),
    "O": (255, 255, 0),
    "J": (255, 165, 0),
    "L": (0, 0, 255),
    "T": (128, 0, 128)
}


class Piece:
    def __init__(self, x, y, shape_key):
        self.x = x
        self.y = y
        self.shape_key = shape_key
        self.shape = SHAPE_FORMATS[shape_key]
        self.color = SHAPE_COLORS[shape_key]
        self.rotation = 0


def create_grid(locked_positions=None):
    if locked_positions is None:
        locked_positions = {}
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    for (x, y), color in locked_positions.items():
        grid[y][x] = color
    return grid


def convert_shape_format(piece):
    positions = []
    shape = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(shape):
        for j, column in enumerate(line):
            if column == '0':
                positions.append((piece.x + j, piece.y + i))

    return [(x - 2, y - 4) for x, y in positions]


def valid_space(piece, grid):
    valid_positions = [(j, i) for i in range(GRID_HEIGHT) for j in range(GRID_WIDTH) if grid[i][j] == BLACK]
    shape_positions = convert_shape_format(piece)
    return all(pos in valid_positions or pos[1] < 0 for pos in shape_positions)


def check_lost(locked_positions):
    return any(y < 1 for x, y in locked_positions)


def get_random_piece():
    return Piece(GRID_WIDTH // 2 - 1, 0, random.choice(list(SHAPE_FORMATS.keys())))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (TOP_LEFT_X + PLAY_WIDTH / 2 - label.get_width() / 2, TOP_LEFT_Y + PLAY_HEIGHT / 2 - label.get_height() / 2))


def draw_grid(surface):
    for i in range(GRID_HEIGHT):
        pygame.draw.line(surface, GRAY, (TOP_LEFT_X, TOP_LEFT_Y + i * BLOCK_SIZE), (TOP_LEFT_X + PLAY_WIDTH, TOP_LEFT_Y + i * BLOCK_SIZE))
    for j in range(GRID_WIDTH):
        pygame.draw.line(surface, GRAY, (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y), (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + PLAY_HEIGHT))


def clear_rows(grid, locked_positions):
    full_rows = [i for i, row in enumerate(grid) if all(cell != BLACK for cell in row)]
    for row in full_rows:
        del locked_positions[(x, row) for x in range(GRID_WIDTH) if (x, row) in locked_positions]

    for (x, y), color in sorted(locked_positions.items(), key=lambda x: x[0][1], reverse=True):
        if y < min(full_rows):
            locked_positions[(x, y + len(full_rows))] = locked_positions.pop((x, y))


def draw_window(surface, grid):
    surface.fill(BLACK)
    draw_grid(surface)
    for i, row in enumerate(grid):
        for j, color in enumerate(row):
            pygame.draw.rect(surface, color, (TOP_LEFT_X + j * BLOCK_SIZE, TOP_LEFT_Y + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def main():
    run = True
    locked_positions = {}
    grid = create_grid(locked_positions)
    current_piece = get_random_piece()
    clock = pygame.time.Clock()
    fall_speed = 0.27
    fall_time = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time / 1000 >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid):
                current_piece.y -= 1
                for pos in convert_shape_format(current_piece):
                    locked_positions[pos] = current_piece.color
                current_piece = get_random_piece()
                if check_lost(locked_positions):
                    run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_window(win, grid)
        pygame.display.update()

    draw_text_middle(win, "Game Over", 40, WHITE)
    pygame.display.update()
    pygame.time.delay(2000)


win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")
main()
pygame.quit()



