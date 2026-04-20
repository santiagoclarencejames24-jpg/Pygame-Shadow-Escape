import pygame
import sys

# Initialize Pygame
pygame.init()

MAP = [
    "#########D###################",
    "#P.....#.....#.....#...#....#",
    "#.#.##...###.#.###.#.#.#.##.#",
    "#.#....#...#...#.#.#.#.#....#",
    "#...#######.#.#.#..#.#.####.#",
    "#.#.......#.#.#.#.#.#.......#",
    "#.#.#####.#.#.#.#.#.#.#####.#",
    "#.#.#...#.#...#.#.#.#.#...#.#",
    "#.#.#.#.#.###.#.#.#.#.#.#.#.#",
    "#...#.#.#.....#...#.#.#.#.#.#",
    "###.#.#.#####.#K###.#.#.#...#",
    "#K..#...#.....#...#.#.#.###.#",
    "#.#.#####.#.#.#.#.#.#.#.....#",
    "#.#.....#.#.#.#.#.#.#.#####.#",
    "#.#.###.#.#.#.#.#.#.#.#.#...#",
    "#.#.#...#.#.#...#.#.#.#.#.#.#",
    "#.#.#.###.#.#####.#.#.#.#.#.#",
    "#.#.......#.......#.#.......#",
    "#############################",
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
DARK_GRAY = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shadow Escape")
clock = pygame.time.Clock()

# Sprite groups
obstacles = pygame.sprite.Group()
players = pygame.sprite.Group()
enemies = pygame.sprite.Group()
doors = pygame.sprite.Group()
keys = pygame.sprite.Group()


def draw_brick_pattern(surface, color):
    """Draw a brick pattern on a surface"""
    surface.fill(DARK_GRAY)
    # Draw brick outline
    pygame.draw.rect(surface, color, (0, 0, TILE_SIZE, TILE_SIZE), 3)
    # Draw brick dividers
    pygame.draw.line(surface, color, (TILE_SIZE // 2, 0), (TILE_SIZE // 2, TILE_SIZE), 1)
    pygame.draw.line(surface, color, (0, TILE_SIZE // 2), (TILE_SIZE, TILE_SIZE // 2), 1)


class Obstacle(pygame.sprite.Sprite):
    """Wall/obstacle sprite"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        draw_brick_pattern(self.image, GRAY)
        self.rect = self.image.get_rect(topleft=(x, y))


class Player(pygame.sprite.Sprite):
    """Player sprite"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("mainCharacter.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE - 10, TILE_SIZE - 10))
        self.rect = self.image.get_rect(center=(x + TILE_SIZE // 2, y + TILE_SIZE // 2))
        self.speed = 2

    def update(self):
        keys = pygame.key.get_pressed()
        old_x = self.rect.x
        old_y = self.rect.y
        
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
            self.rect.x = old_x
            self.rect.y = old_y


class Enemy(pygame.sprite.Sprite):
    """Enemy sprite"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("ghost.png")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1.5
        self.target_player = None
    
    def update(self):
        if self.target_player:
            old_x = self.rect.x
            old_y = self.rect.y
            
            # Chase the player
            dx = self.target_player.rect.centerx - self.rect.centerx
            dy = self.target_player.rect.centery - self.rect.centery
            distance = (dx**2 + dy**2)**0.5
            
            if distance > 0:
                # Normalize and apply speed
                self.rect.x += (dx / distance) * self.speed
                self.rect.y += (dy / distance) * self.speed
            
            # Collision detection with obstacles
            if pygame.sprite.spritecollideany(self, obstacles):
                self.rect.x = old_x
                self.rect.y = old_y


class Door(pygame.sprite.Sprite):
    """Door/exit sprite"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect(topleft=(x, y))


class Key(pygame.sprite.Sprite):
    """Collectible key sprite"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        # Draw a key shape (simple representation)
        pygame.draw.circle(self.image, YELLOW, (TILE_SIZE // 2, TILE_SIZE // 2), TILE_SIZE // 4)
        pygame.draw.rect(self.image, YELLOW, (TILE_SIZE // 2, TILE_SIZE // 2 - 2, TILE_SIZE // 3, 4))
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

# Set player as target for all enemies
for enemy in enemies:
    enemy.target_player = player

# Add some collectible keys
key_positions = [(5 * TILE_SIZE, 5 * TILE_SIZE), (10 * TILE_SIZE, 10 * TILE_SIZE), (15 * TILE_SIZE, 5 * TILE_SIZE)]
for key_x, key_y in key_positions:
    keys.add(Key(key_x, key_y))

# Start screen
def show_start_screen():
    """Display the start screen"""
    font_title = pygame.font.Font(None, 100)
    font_subtitle = pygame.font.Font(None, 40)
    font_button = pygame.font.Font(None, 50)
    font_info = pygame.font.Font(None, 30)
    
    start_screen_running = True
    button_animation = 0
    
    while start_screen_running:
        clock.tick(FPS)
        button_animation = (button_animation + 1) % 60
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                start_screen_running = False
        
        screen.fill(BLACK)
        
        # Draw gradient-like background with rectangles
        for i in range(0, SCREEN_HEIGHT, 40):
            alpha = int(20 * (1 + 0.2 * (button_animation / 30)))
            pygame.draw.line(screen, (50, 50, 100), (0, i), (SCREEN_WIDTH, i), 2)
        
        # Title
        title_text = font_title.render("Shadow Escape", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_text, title_rect)
        
        # Decorative line
        pygame.draw.line(screen, YELLOW, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 + 80), 
                        (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT // 4 + 80), 3)
        
        # Subtitle
        subtitle_text = font_subtitle.render("Escape from the shadows!", True, WHITE)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 60))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Game instructions
        
        
        info_text2 = font_info.render("Avoid the ghosts! Collect all keys!", True, WHITE)
        info_rect2 = info_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        screen.blit(info_text2, info_rect2)
        
        # Start button with animation
        button_width = 300
        button_height = 80
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y = 2 * SCREEN_HEIGHT // 3
        
        # Animate button size
        button_scale = 1 + 0.1 * (button_animation / 30)
        current_width = int(button_width * button_scale)
        current_height = int(button_height * button_scale)
        current_x = SCREEN_WIDTH // 2 - current_width // 2
        current_y = button_y - (current_height - button_height) // 2
        
        # Draw button background
        pygame.draw.rect(screen, YELLOW, (current_x, current_y, current_width, current_height), 3)
        pygame.draw.rect(screen, (50, 50, 50), (current_x + 5, current_y + 5, current_width - 10, current_height - 10))
        
        # Button text
        button_text = font_button.render("Press T to Start", True, YELLOW)
        button_text_rect = button_text.get_rect(center=(SCREEN_WIDTH // 2, button_y + button_height // 2))
        screen.blit(button_text, button_text_rect)
        
        pygame.display.flip()

show_start_screen()

# Game loop
running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update
    players.update()
    enemies.update()
    
    # Draw
    screen.fill(BLACK)
    obstacles.draw(screen)
    doors.draw(screen)
    keys.draw(screen)
    enemies.draw(screen)
    players.draw(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()