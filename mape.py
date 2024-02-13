import pygame
import math

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 25
GRID_WIDTH, GRID_HEIGHT = WIDTH // GRID_SIZE, HEIGHT // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level Editor")

# Define colors
WHITE = 0
BLACK = 1
RED = 2
GREEN = 3
BLUE = 4

# Button parameters
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 40
SAVE_BUTTON_POS = (10, 10)
LOAD_BUTTON_POS = (120, 10)
SAVE_BUTTON_COLOR = (50, 205, 50)  # LimeGreen
LOAD_BUTTON_COLOR = (65, 105, 225)  # RoyalBlue

# Initialize map
MAP = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text

    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont(None, 20)
            text = font.render(self.text, 1, (0, 0, 0))
            screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2),
                               self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False

# Create buttons
save_button = Button(SAVE_BUTTON_POS[0], SAVE_BUTTON_POS[1], BUTTON_WIDTH, BUTTON_HEIGHT, SAVE_BUTTON_COLOR, 'Save')
load_button = Button(LOAD_BUTTON_POS[0], LOAD_BUTTON_POS[1], BUTTON_WIDTH, BUTTON_HEIGHT, LOAD_BUTTON_COLOR, 'Load')

# Main game loop
running = True
drawing = False
draw_color = BLACK  # Default draw color
while running:
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                drawing = True
            # Check if save button or load button is clicked
            if save_button.is_over(pygame.mouse.get_pos()):
                with open("map.txt", "w") as file:
                    for row in MAP:
                        file.write("".join(map(str, row)) + "\n")
            elif load_button.is_over(pygame.mouse.get_pos()):
                with open("map.txt", "r") as file:
                    for i, line in enumerate(file):
                        MAP[i] = list(map(int, line.strip()))
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_2:  # Change draw color to red
                draw_color = RED
            elif event.key == pygame.K_3:  # Change draw color to green
                draw_color = GREEN
            elif event.key == pygame.K_4:  # Change draw color to blue
                draw_color = BLUE
            elif event.key == pygame.K_1:  # Change draw color to black
                draw_color = BLACK
            elif event.key == pygame.K_0:  # Change draw color to white
                draw_color = WHITE

    # Draw grid
    colorwhite = (255, 255, 255)
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = colorwhite
            if MAP[y][x] == RED:
                color = (255, 0, 0)  # Red
            elif MAP[y][x] == GREEN:
                color = (0, 255, 0)  # Green
            elif MAP[y][x] == BLUE:
                color = (0, 0, 255)  # Blue
            if MAP[y][x] == BLACK:
                color = (0, 0, 0)  # black
            elif MAP[y][x] == WHITE:
                color = (255, 255, 255)  # white
            
            pygame.draw.rect(screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 0)
            pygame.draw.rect(screen, BLACK, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)

    # Draw buttons
    save_button.draw(screen, BLACK)
    load_button.draw(screen, BLACK)

    # Update map based on mouse input
    if drawing:
        mouse_pos = pygame.mouse.get_pos()
        grid_x, grid_y = mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE
        if 0 <= grid_x < GRID_WIDTH and 0 <= grid_y < GRID_HEIGHT:
            MAP[grid_y][grid_x] = draw_color

    # Draw cursor
    mouse_pos = pygame.mouse.get_pos()
    grid_x, grid_y = mouse_pos[0] // GRID_SIZE, mouse_pos[1] // GRID_SIZE
    pygame.draw.rect(screen, draw_color, (grid_x * GRID_SIZE, grid_y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 2)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
