import pygame
import math

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Raycasting")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
thisisatest5 = (52, 71 ,74)
thisisatest6 = (21, 21 ,83)
thisisatest7 = (67, 24 ,25)
thisisatest8 = (1, 12 ,56)
thisisatest9 = (53, 3 ,25)

# Define color mappings based on map data
COLOR_MAP = {
    '0': WHITE,
    '1': BLACK,
    '2': RED,
    '3': GREEN,
    '4': BLUE,
    '5': thisisatest5,
    '6': thisisatest6,
    '7': thisisatest7,
    '8': thisisatest8,
    '9': thisisatest9
}

# Define player parameters
player_pos = [WIDTH / 2, HEIGHT / 2]
player_angle = 0
FOV = math.pi / 2
NUM_RAYS = 30
RAY_ANGLE_INCREMENT = FOV / NUM_RAYS

# Load map from file
def load_map(file_name):
    with open("map.txt", 'r') as file:
        return [line.strip() for line in file]

loaded_map = load_map("map.txt")
MAP_WIDTH = len(loaded_map[0])
MAP_HEIGHT = len(loaded_map)

# Function to cast rays
def cast_rays():
    ray_angle = player_angle - FOV / 2
    for i in range(NUM_RAYS):
        # Ray direction
        ray_dx = math.cos(ray_angle)
        ray_dy = math.sin(ray_angle)

        # Ray position
        ray_x, ray_y = player_pos

        # Cast ray until it hits a wall
        while True:
            ray_x += ray_dx
            ray_y += ray_dy

            # Check for collision with wall
            cell_x = int(ray_x / (WIDTH / MAP_WIDTH))
            cell_y = int(ray_y / (HEIGHT / MAP_HEIGHT))
            if cell_x < 0 or cell_x >= MAP_WIDTH or cell_y < 0 or cell_y >= MAP_HEIGHT or loaded_map[cell_y][cell_x] != '0':
                break

        # Calculate distance to wall
        distance_to_wall = math.sqrt((ray_x - player_pos[0])**2 + (ray_y - player_pos[1])**2)

        # Determine wall color
        wall_color = WHITE
        if cell_x >= 0 and cell_x < MAP_WIDTH and cell_y >= 0 and cell_y < MAP_HEIGHT:
            cell_value = loaded_map[cell_y][cell_x]
            if cell_value in COLOR_MAP:
                wall_color = COLOR_MAP[cell_value]

        # Calculate wall height based on distance
        wall_height = min(400, int(HEIGHT * 70 / distance_to_wall))

        # Draw wall
        pygame.draw.rect(screen, wall_color, (WIDTH / NUM_RAYS * i, HEIGHT / 2 - wall_height / 2, WIDTH / NUM_RAYS, wall_height))

        # Increment angle for next ray
        ray_angle += RAY_ANGLE_INCREMENT


# Main game loop
running = True
MAP = load_map("map.txt")  # Load map from file
MAP_WIDTH = len(MAP[0])
MAP_HEIGHT = len(MAP)
while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player controls
    keys = pygame.key.get_pressed()
    movement_speed = 2  # Adjust this as needed
    rotation_speed = 0.05  # Adjust this as needed
    if keys[pygame.K_LEFT]:
        player_angle -= rotation_speed
    if keys[pygame.K_RIGHT]:
        player_angle += rotation_speed
    if keys[pygame.K_UP]:
        # Move the player in the direction they are facing
        player_pos[0] += math.cos(player_angle) * movement_speed
        player_pos[1] += math.sin(player_angle) * movement_speed
    if keys[pygame.K_DOWN]:
        # Move the player backward (opposite direction they are facing)
        player_pos[0] -= math.cos(player_angle) * movement_speed
        player_pos[1] -= math.sin(player_angle) * movement_speed

    # Cast rays
    cast_rays()

    # Draw player
    pygame.draw.circle(screen, RED, (int(player_pos[0]), int(player_pos[1])), 0)

    pygame.display.flip()

# Quit Pygame
pygame.quit()
