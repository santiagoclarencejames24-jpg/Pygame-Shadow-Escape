import pygame
import sys

# Initialize Pygame
pygame.init()

MAP = [
    "#########D#########",
    "#P.....#.....#.....#",
    "#.#.##...###.#.###.#",
    "#.#....#...#...#.#.#",
    "#...#######.#.#.#..#",
    "#.#.......#.#.#.#.#",
    "#.#.#####.#.#.#.#.#",
    "#.#.#...#.#...#.#.#",
    "#.#.#.#.#.###.#.#.#",
    "#...#.#.#.....#...#",
    "###.#.#.#####.#K###",
    "#K..#...#.....#...#",
    "#.#.#####.#.#.#.#.#",
    "#.#.....#.#.#.#.#.#",
    "#.#.###.#.#.#.#.#.#",
    "#.#.#...#.#.#...#.#",
    "#.#.#.###.#.#####.#",
    "#.#.......#.......#",
    "#.#.#########.#####",
    "#...#.........#....#",
]

# Constants
TILE_SIZE = 32
SCREEN_WIDTH = len(MAP[0]) * TILE_SIZE
SCREEN_HEIGHT = len(MAP) * TILE_SIZE
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Maze Game")
clock = pygame.time.Clock()

# Sprite groups
obstacles = pygame.sprite.Group()
players = pygame.sprite.Group()
enemies = pygame.sprite.Group()
doors = pygame.sprite.Group()


class Obstacle(pygame.sprite.Sprite):
    """Wall/obstacle sprite"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(topleft=(x, y))


class Player(pygame.sprite.Sprite):
    """Player sprite"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        
        # Collision detection with obstacles
        if pygame.sprite.spritecollideany(self, obstacles):
            if keys[pygame.K_LEFT]:
                self.rect.x += self.speed
            if keys[pygame.K_RIGHT]:
                self.rect.x -= self.speed
            if keys[pygame.K_UP]:
                self.rect.y += self.speed
            if keys[pygame.K_DOWN]:
                self.rect.y -= self.speed


class Enemy(pygame.sprite.Sprite):
    """Enemy sprite"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))


class Door(pygame.sprite.Sprite):
    """Door/exit sprite"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))


# Parse map and create sprites
player = None
for y, row in enumerate(MAP):
    for x, char in enumerate(row):
        pos_x = x * TILE_SIZE
        pos_y = y * TILE_SIZE
        
        if char == "#":
            obstacles.add(Obstacle(pos_x, pos_y))
        elif char == "P":
            player = Player(pos_x, pos_y)
            players.add(player)
        elif char == "K":
            enemies.add(Enemy(pos_x, pos_y))
        elif char == "D":
            doors.add(Door(pos_x, pos_y))

# Game loop
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update
    players.update()
    
    # Draw
    screen.fill(BLACK)
    obstacles.draw(screen)
    doors.draw(screen)
    enemies.draw(screen)
    players.draw(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()