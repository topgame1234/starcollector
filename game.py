import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star Collector")

# Colors
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
YELLOW = (255, 255, 0)

# Player properties
player_size = 40
player_x = WIDTH // 2
player_y = HEIGHT - player_size
player_speed = 5
player_jump = -15
player_velocity = 0
gravity = 0.8

# Star properties
star_size = 20
stars = []
score = 0

# Create initial stars
for _ in range(5):
    stars.append([random.randint(0, WIDTH - star_size), random.randint(0, HEIGHT//2), star_size])

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_y >= HEIGHT - player_size:
                player_velocity = player_jump

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
        player_x += player_speed

    # Apply gravity
    player_velocity += gravity
    player_y += player_velocity
    
    # Ground collision
    if player_y > HEIGHT - player_size:
        player_y = HEIGHT - player_size
        player_velocity = 0

    # Check star collection
    for star in stars[:]:
        if (player_x < star[0] + star[2] and 
            player_x + player_size > star[0] and
            player_y < star[1] + star[2] and
            player_y + player_size > star[1]):
            stars.remove(star)
            score += 1
            stars.append([random.randint(0, WIDTH - star_size), 
                        random.randint(0, HEIGHT//2), 
                        star_size])

    # Draw everything
    screen.fill(BLUE)
    
    # Draw player (cute square with eyes)
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_size, player_size))
    pygame.draw.circle(screen, (0, 0, 0), (player_x + 10, player_y + 15), 5)  # Left eye
    pygame.draw.circle(screen, (0, 0, 0), (player_x + 30, player_y + 15), 5)  # Right eye
    
    # Draw stars
    for star in stars:
        pygame.draw.polygon(screen, YELLOW, [
            (star[0] + star[2]//2, star[1]),
            (star[0] + star[2], star[1] + star[2]//2),
            (star[0] + star[2]//2, star[1] + star[2]),
            (star[0], star[1] + star[2]//2)
        ])

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()