import pygame
import random
import pyautogui
from screeninfo import get_monitors  # Fallback for resolution detection

# Try to detect screen resolution using pyautogui, fall back to screeninfo
try:
    screen_width, screen_height = pyautogui.size()
except:
    monitor = get_monitors()[0]  # Use primary monitor
    screen_width = monitor.width
    screen_height = monitor.height

# Set game resolution to half of screen resolution
WIDTH, HEIGHT = screen_width // 2, screen_height // 2
print(f"Detected screen resolution: {screen_width}x{screen_height}")
print(f"Game resolution: {WIDTH}x{HEIGHT}")

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Space Invaders")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Calculate scaling factor based on assumed original 800x600 -> half resolution
scale_factor = WIDTH / 400  # Assuming original half-res is 400x300 from 800x600

# Player settings (8x8 pixel design, matching your previous request)
player_width = int(8 * scale_factor)
player_height = int(8 * scale_factor)
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - int(20 * scale_factor)
player_speed = 2.5 * scale_factor

# Player pixel pattern (8x8, wider base, narrower middle, pointed top)
player_pattern = [
    (2, 0), (3, 0), (4, 0), (5, 0),  # Top point (4 pixels wide)
    (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),  # Middle (6 pixels wide)
    (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2),  # Base (8 pixels wide)
    (0, 3), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3),  # Base (8 pixels wide)
    (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4),  # Base (8 pixels wide)
    (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5),  # Base (8 pixels wide)
    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6),  # Base (8 pixels wide)
    (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)   # Base (8 pixels wide)
]

# Bullet settings
bullet_width = int(1 * scale_factor)
bullet_height = int(5 * scale_factor)
bullet_speed = 3.5 * scale_factor
bullets = []  # Player bullets
enemy_bullets = []  # Enemy bullets
fire_cooldown = 0.5
last_shot = 0

# Enemy settings (classic alien designs, exact 8x8 pixel art)
alien_base_size = 8  # Original pixel size (8x8)
alien_pixel_size = int(1 * scale_factor)  # Use 1x1 pixels for each original pixel
alien_width = alien_base_size * alien_pixel_size  # Width of each alien
alien_height = alien_base_size * alien_pixel_size
alien_types = [
    [GREEN, [  # Squid (top and bottom rows)
        (1, 0), (2, 0), (5, 0), (6, 0),  # Top row
        (0, 1), (3, 1), (4, 1), (7, 1),  # 2nd row
        (1, 2), (2, 2), (5, 2), (6, 2),  # 3rd row
        (0, 3), (3, 3), (4, 3), (7, 3),  # 4th row
        (1, 4), (2, 4), (5, 4), (6, 4),  # 5th row
        (0, 5), (3, 5), (4, 5), (7, 5),  # 6th row
        (1, 6), (2, 6), (5, 6), (6, 6),  # 7th row
        (0, 7), (7, 7)                   # Bottom row
    ]],
    [CYAN, [  # Crab (2nd row)
        (1, 0), (2, 0), (5, 0), (6, 0),  # Top row
        (0, 1), (3, 1), (4, 1), (7, 1),  # 2nd row
        (0, 2), (7, 2),                   # 3rd row
        (0, 3), (1, 3), (2, 3), (5, 3), (6, 3), (7, 3),  # 4th row
        (1, 4), (2, 4), (5, 4), (6, 4),  # 5th row
        (2, 5), (5, 5),                   # 6th row
        (3, 6), (4, 6),                   # 7th row
        (2, 7), (5, 7)                    # Bottom row
    ]],
    [MAGENTA, [  # Octopus (3rd row)
        (1, 0), (2, 0), (5, 0), (6, 0),  # Top row
        (0, 1), (3, 1), (4, 1), (7, 1),  # 2nd row
        (0, 2), (7, 2),                   # 3rd row
        (0, 3), (7, 3),                   # 4th row
        (0, 4), (1, 4), (2, 4), (5, 4), (6, 4), (7, 4),  # 5th row
        (1, 5), (2, 5), (5, 5), (6, 5),  # 6th row
        (2, 6), (5, 6),                   # 7th row
        (3, 7), (4, 7)                    # Bottom row
    ]],
    [YELLOW, [  # Crab (4th row, same as 2nd row)
        (1, 0), (2, 0), (5, 0), (6, 0),  # Top row
        (0, 1), (3, 1), (4, 1), (7, 1),  # 2nd row
        (0, 2), (7, 2),                   # 3rd row
        (0, 3), (1, 3), (2, 3), (5, 3), (6, 3), (7, 3),  # 4th row
        (1, 4), (2, 4), (5, 4), (6, 4),  # 5th row
        (2, 5), (5, 5),                   # 6th row
        (3, 6), (4, 6),                   # 7th row
        (2, 7), (5, 7)                    # Bottom row
    ]],
    [GREEN, [  # Squid (bottom row, same as top row)
        (1, 0), (2, 0), (5, 0), (6, 0),  # Top row
        (0, 1), (3, 1), (4, 1), (7, 1),  # 2nd row
        (1, 2), (2, 2), (5, 2), (6, 2),  # 3rd row
        (0, 3), (3, 3), (4, 3), (7, 3),  # 4th row
        (1, 4), (2, 4), (5, 4), (6, 4),  # 5th row
        (0, 5), (3, 5), (4, 5), (7, 5),  # 6th row
        (1, 6), (2, 6), (5, 6), (6, 6),  # 7th row
        (0, 7), (7, 7)                   # Bottom row
    ]]
]
enemy_speed = 1 * scale_factor
enemy_drop_distance = 0.5 * scale_factor  # Significantly increased drop speed for faster drops
enemies = []
for row, (color, pattern) in enumerate(alien_types):
    for col in range(11):  # 11 aliens per row
        x = int(25 * scale_factor) + col * (alien_width + int(15 * scale_factor))  # Adjusted spacing
        y = int(25 * scale_factor) + row * (alien_height + int(15 * scale_factor))  # Adjusted vertical spacing
        enemies.append([x, y, color, pattern])
enemy_fire_rate = 2.0
last_enemy_shot = 0

# Bunker settings (bold 18x12 pixel design, matching your image)
bunker_width = int(18 * scale_factor)
bunker_height = int(12 * scale_factor)
bunker_sections_height = bunker_height // 3
bunker_pixel_size = int(2 * scale_factor)  # Make each pixel 2x2 or larger for boldness
bunkers = [
    [WIDTH // 4 - bunker_width // 2, HEIGHT - int(50 * scale_factor)],
    [WIDTH // 2 - bunker_width // 2, HEIGHT - int(50 * scale_factor)],
    [3 * WIDTH // 4 - bunker_width // 2, HEIGHT - int(50 * scale_factor)]
]
bunker_health = [[3, 3, 3] for _ in range(3)]  # [top, middle, bottom] health for each bunker

# Bunker pixel pattern (18x12, based on your image: wide base, narrower middle, arched top, bold)
bunker_pattern = [
    # Top (arched, bold, 8-10 pixels wide)
    (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0),  # Arched top (8 pixels wide)
    (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1),  # Wider middle (10 pixels)
    (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (13, 2),  # Wider (12 pixels)
    # Middle (narrower, 12-14 pixels wide)
    (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (12, 3), (13, 3), (14, 3),  # 14 pixels
    (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (11, 4), (12, 4), (13, 4), (14, 4),  # 14 pixels
    (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5), (8, 5), (9, 5), (10, 5), (11, 5), (12, 5), (13, 5), (14, 5), (15, 5), (16, 5), (17, 5),  # Base (18 pixels)
    (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6), (8, 6), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (15, 6), (16, 6), (17, 6),  # Base (18 pixels)
    (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (8, 7), (9, 7), (10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (17, 7),  # Base (18 pixels)
    (0, 8), (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8), (8, 8), (9, 8), (10, 8), (11, 8), (12, 8), (13, 8), (14, 8), (15, 8), (16, 8), (17, 8),  # Base (18 pixels)
    (0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (6, 9), (7, 9), (8, 9), (9, 9), (10, 9), (11, 9), (12, 9), (13, 9), (14, 9), (15, 9), (16, 9), (17, 9),  # Base (18 pixels)
    (0, 10), (1, 10), (2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10), (8, 10), (9, 10), (10, 10), (11, 10), (12, 10), (13, 10), (14, 10), (15, 10), (16, 10), (17, 10),  # Base (18 pixels)
    (0, 11), (1, 11), (2, 11), (3, 11), (4, 11), (5, 11), (6, 11), (7, 11), (8, 11), (9, 11), (10, 11), (11, 11), (12, 11), (13, 11), (14, 11), (15, 11), (16, 11), (17, 11)  # Base (18 pixels)
]

# Player lives
lives = 3
life_icon_size = int(8 * scale_factor)  # Scaled down

# Starry background
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(int(25 * scale_factor))]  # Fewer stars, scaled

# Score and high score
score = 0
high_score = 1660  # Default high score from your screenshot

# Game loop control
clock = pygame.time.Clock()
running = True

def draw_alien(x, y, color, pattern):
    # Draw exact pixel art for alien (8x8 grid, 1x1 pixels per original pixel)
    for px, py in pattern:
        pygame.draw.rect(screen, color, 
                        (x + px * alien_pixel_size, y + py * alien_pixel_size, 
                         alien_pixel_size, alien_pixel_size))

def draw_player(x, y):
    # Draw exact pixel art for player (scaled 8x8 grid, new design)
    for px, py in player_pattern:
        pygame.draw.rect(screen, GREEN, 
                        (x + px * alien_pixel_size, y + py * alien_pixel_size, 
                         alien_pixel_size, alien_pixel_size))

def draw_bunker(x, y, health):
    # Draw bold pixel art for bunker (18x12 grid, 2x2 pixels per original pixel)
    sections = [
        (x, y, bunker_width, bunker_sections_height),  # Top
        (x, y + bunker_sections_height, bunker_width, bunker_sections_height),  # Middle
        (x, y + 2 * bunker_sections_height, bunker_width, bunker_sections_height)  # Bottom
    ]
    for i, (bx, by, bw, bh) in enumerate(sections):
        if health[i] > 0:
            # Draw only undamaged pixels from bunker_pattern, bolder
            for px, py in bunker_pattern:
                if (py >= i * bunker_sections_height // bunker_pixel_size and 
                    py < (i + 1) * bunker_sections_height // bunker_pixel_size):
                    pygame.draw.rect(screen, GREEN, 
                                    (bx + px * bunker_pixel_size, by + (py % (bunker_sections_height // bunker_pixel_size)) * bunker_pixel_size, 
                                     bunker_pixel_size, bunker_pixel_size))
        else:
            pygame.draw.rect(screen, BLACK, (bx, by, bw, bh))  # Damaged area turns black

def draw_stars():
    for star_x, star_y in stars:
        pygame.draw.rect(screen, WHITE, (star_x, star_y, 1, 1))

def draw_lives():
    # Draw lives as small spaceship icons in bottom-left, matching screenshot, using new player design
    for i in range(lives):
        offset = i * (life_icon_size + int(5 * scale_factor))
        draw_player(int(5 * scale_factor) + offset, HEIGHT - int(15 * scale_factor))  # Position at bottom-left

def draw_scores():
    # Draw score and high score like original
    font = pygame.font.SysFont(None, int(12 * scale_factor))  # Scaled font
    score_text = font.render(f"SCORE: {score}", True, WHITE)
    high_score_text = font.render(f"HIGHSCORE: {high_score}", True, WHITE)
    screen.blit(score_text, (int(5 * scale_factor), int(5 * scale_factor)))  # Top-left
    screen.blit(high_score_text, (WIDTH - int(100 * scale_factor), int(5 * scale_factor)))  # Top-right

while running:
    current_time = pygame.time.get_ticks() / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if current_time - last_shot >= fire_cooldown:
                bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y])
                last_shot = current_time

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Update player bullets
    for bullet in bullets[:]:
        bullet[1] -= bullet_speed
        if bullet[1] < 0:
            bullets.remove(bullet)

    # Update enemy bullets
    for bullet in enemy_bullets[:]:
        bullet[1] += bullet_speed
        if bullet[1] > HEIGHT:
            enemy_bullets.remove(bullet)

    # Enemy movement and shooting
    edge_hit = False
    for enemy in enemies[:]:
        enemy[0] += enemy_speed
        if enemy[0] > WIDTH - alien_width or enemy[0] < 0:
            edge_hit = True

    if edge_hit:
        enemy_speed = -enemy_speed
        for enemy in enemies:
            if enemy:  # Ensure enemy exists
                enemy[1] += enemy_drop_distance  # Much faster drop

    if current_time - last_enemy_shot >= enemy_fire_rate and enemies:
        shooter = random.choice([e for e in enemies if e])  # Ensure valid shooter
        if shooter:
            enemy_bullets.append([shooter[0] + alien_width // 2 - bullet_width // 2, shooter[1] + alien_height])
            last_enemy_shot = current_time

    # Collision detection
    for bullet in bullets[:]:
        for enemy in [e for e in enemies if e]:  # Only valid enemies
            if (bullet[0] > enemy[0] and bullet[0] < enemy[0] + alien_width and
                bullet[1] > enemy[1] and bullet[1] < enemy[1] + alien_height):
                if bullet in bullets:
                    bullets.remove(bullet)
                enemies[enemies.index(enemy)] = None  # Mark as removed
                score += 10
                # Update high score if necessary
                if score > high_score:
                    high_score = score
                break
        for i, bunker in enumerate(bunkers[:]):
            if all(h <= 0 for h in bunker_health[i]):  # Skip if bunker is fully destroyed
                continue
            # Check if bullet hits bunker
            if (bullet[0] > bunker[0] and bullet[0] < bunker[0] + bunker_width and
                bullet[1] > bunker[1] and bullet[1] < bunker[1] + bunker_height):
                # Check if player is beneath bunker
                player_beneath = (player_x < bunker[0] + bunker_width and 
                                 player_x + player_width > bunker[0] and 
                                 player_y + player_height > bunker[1])
                if player_beneath:
                    # Damage bottom section if player is beneath
                    if bunker_health[i][2] > 0 and bullet in bullets:
                        bullets.remove(bullet)
                        bunker_health[i][2] -= 1
                else:
                    # Allow bullet to pass if it doesn’t hit an undamaged section
                    hit_section = False
                    sections = [
                        (bunker[1], bunker[1] + bunker_sections_height),  # Top
                        (bunker[1] + bunker_sections_height, bunker[1] + 2 * bunker_sections_height),  # Middle
                        (bunker[1] + 2 * bunker_sections_height, bunker[1] + bunker_height)  # Bottom
                    ]
                    for j, (start_y, end_y) in enumerate(sections):
                        if bullet[1] > start_y and bullet[1] < end_y and bunker_health[i][j] > 0:
                            hit_section = True
                            if bullet in bullets:
                                bullets.remove(bullet)
                                bunker_health[i][j] -= 1
                                break
                    if not hit_section and bullet in bullets:
                        # Bullet passes through if it doesn’t hit an undamaged section
                        continue

    for bullet in enemy_bullets[:]:
        if (bullet[0] > player_x and bullet[0] < player_x + player_width and
            bullet[1] > player_y and bullet[1] < player_y + player_height):
            if lives > 0:
                lives -= 1  # Lose a life
                if bullet in enemy_bullets:
                    enemy_bullets.remove(bullet)  # Remove the bullet
                if lives == 0:
                    running = False  # Game over if no lives left
            else:
                running = False  # Game over immediately if no lives
        for i, bunker in enumerate(bunkers[:]):
            if all(h <= 0 for h in bunker_health[i]):  # Skip if bunker is fully destroyed
                continue
            if (bullet[0] > bunker[0] and bullet[0] < bunker[0] + bunker_width and
                bullet[1] > bunker[1] and bullet[1] < bunker[1] + bunker_height):
                # Enemy bullets always damage from the top down
                if bunker_health[i][0] > 0 and bullet in enemy_bullets:
                    enemy_bullets.remove(bullet)
                    bunker_health[i][0] -= 1
                elif bunker_health[i][1] > 0 and bullet in enemy_bullets:
                    enemy_bullets.remove(bullet)
                    bunker_health[i][1] -= 1
                elif bunker_health[i][2] > 0 and bullet in enemy_bullets:
                    enemy_bullets.remove(bullet)
                    bunker_health[i][2] -= 1

    # Game over if enemies reach bottom
    for enemy in [e for e in enemies if e]:
        if enemy[1] > HEIGHT - alien_height:
            running = False

    # Respawn enemies (clean None values)
    enemies = [e for e in enemies if e]  # Remove None values
    if not enemies:
        enemies = []
        for row, (color, pattern) in enumerate(alien_types):
            for col in range(11):
                x = int(25 * scale_factor) + col * (alien_width + int(15 * scale_factor))  # Adjusted spacing
                y = int(25 * scale_factor) + row * (alien_height + int(15 * scale_factor))
                enemies.append([x, y, color, pattern])

    # Draw everything
    screen.fill(BLACK)  # Clear screen completely each frame
    draw_stars()  # Draw starry background
    draw_player(player_x, player_y)  # Draw classic spaceship
    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, (bullet[0], bullet[1], bullet_width, bullet_height))  # Player bullets
    for bullet in enemy_bullets:
        pygame.draw.rect(screen, RED, (bullet[0], bullet[1], bullet_width, bullet_height))  # Enemy bullets
    for enemy in [e for e in enemies if e]:  # Only draw valid enemies
        draw_alien(enemy[0], enemy[1], enemy[2], enemy[3])  # Draw classic alien
    for i, bunker in enumerate(bunkers):
        draw_bunker(bunker[0], bunker[1], bunker_health[i])  # Draw bunker with sections

    # Display scores and lives
    draw_scores()  # Draw score and high score
    draw_lives()  # Draw lives at bottom-left

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Game over
font = pygame.font.SysFont(None, int(37 * scale_factor))  # Scaled font
game_over_text = font.render("Game Over", True, WHITE)
screen.blit(game_over_text, (WIDTH // 2 - int(75 * scale_factor), HEIGHT // 2 - int(20 * scale_factor)))
pygame.display.flip()
pygame.time.wait(2000)
pygame.quit()