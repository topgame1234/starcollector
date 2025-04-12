import pygame
import random
import sys
import math

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
RED = (255, 0, 0)  # Color for enemy
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)  # Color for bullets
LIGHT_BLUE = (173, 216, 230)
GRASS_GREEN = (34, 139, 34)  # Dark green for grass

# Visual effects
particles = []
class Particle:
    def __init__(self, x, y, color, size, speed_x, speed_y, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.lifetime = lifetime
        self.age = 0

# Background elements
clouds = []
for _ in range(5):
    clouds.append([
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT//2),
        random.randint(50, 100)  # cloud size
    ])

# Grass properties
grass_blades = []
GRASS_HEIGHT = 20
GRASS_SPACING = 5
for x in range(0, WIDTH, GRASS_SPACING):
    height_variation = random.randint(-5, 5)
    grass_blades.append([x, HEIGHT - GRASS_HEIGHT + height_variation])

# Player properties
player_size = 40
player_x = WIDTH // 2
player_y = HEIGHT - player_size
player_speed = 5
player_jump = -15
player_velocity = 0
gravity = 0.8

# Bullet properties
bullets = []
bullet_speed = 10
bullet_size = 8

# Enemy properties
enemy_size = 30
enemy_x = random.randint(0, WIDTH - enemy_size)
enemy_y = random.randint(0, HEIGHT - enemy_size)
enemy_speed = 3
enemy_direction = random.choice([-1, 1])  # Random initial direction

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
            if event.key == pygame.K_w:  # Jump on W press
                player_velocity = player_jump
        if event.type == pygame.MOUSEBUTTONDOWN:  # Change to mouse control
            if event.button == 1:  # Left click
                bullets.append([
                    player_x + player_size // 2 - bullet_size // 2,
                    player_y + player_size // 2 - bullet_size // 2,
                ])

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_x > 0:  # A key for left
        player_x -= player_speed
    if keys[pygame.K_d] and player_x < WIDTH - player_size:  # D key for right
        player_x += player_speed

    # Apply gravity
    player_velocity += gravity
    player_y += player_velocity
    
    # Ground collision
    if player_y > HEIGHT - player_size:
        player_y = HEIGHT - player_size
        player_velocity = 0

    # Move enemy
    enemy_x += enemy_speed * enemy_direction
    
    # Enemy bounds checking and direction change
    if enemy_x <= 0:
        enemy_x = 0
        enemy_direction = 1
    elif enemy_x >= WIDTH - enemy_size:
        enemy_x = WIDTH - enemy_size
        enemy_direction = -1
    
    # Check enemy collision
    if (player_x < enemy_x + enemy_size and 
        player_x + player_size > enemy_x and 
        player_y < enemy_y + enemy_size and 
        player_y + player_size > enemy_y):
        running = False  # Game over on enemy collision

    # Check star collection - fixing collision detection
    for star in stars[:]:
        if (player_x + player_size > star[0] and 
            player_x < star[0] + star[2] and
            player_y + player_size > star[1] and
            player_y < star[1] + star[2]):
            stars.remove(star)
            score += 1
            # Spawn new star at random position
            stars.append([
                random.randint(0, WIDTH - star_size),
                random.randint(0, HEIGHT//2),
                star_size
            ])

    # Update particles
    for particle in particles[:]:
        particle.x += particle.speed_x
        particle.y += particle.speed_y
        particle.age += 1
        if particle.age >= particle.lifetime:
            particles.remove(particle)

    # Update and draw bullets with particles
    for bullet in bullets[:]:
        bullet[0] += bullet_speed  # Move bullet right
        # Create trailing particles
        if random.random() < 0.3:  # 30% chance each frame
            particles.append(Particle(
                bullet[0] + bullet_size//2,
                bullet[1] + bullet_size//2,
                ORANGE,
                random.randint(2, 4),
                random.uniform(-1, 1),
                random.uniform(-1, 1),
                20
            ))
        # Remove bullet if it goes off screen
        if bullet[0] > WIDTH:
            bullets.remove(bullet)
        # Check bullet collision with enemy
        elif (bullet[0] < enemy_x + enemy_size and
              bullet[0] + bullet_size > enemy_x and
              bullet[1] < enemy_y + enemy_size and
              bullet[1] + bullet_size > enemy_y):
            bullets.remove(bullet)
            # Respawn enemy at random position on the left side
            enemy_x = -enemy_size
            enemy_y = random.randint(0, HEIGHT - enemy_size)
            score += 2  # Bonus points for hitting enemy

    # Move clouds
    for cloud in clouds:
        cloud[0] -= 0.5  # Slow movement left
        if cloud[0] + cloud[2] < 0:
            cloud[0] = WIDTH
            cloud[1] = random.randint(0, HEIGHT//2)

    # Draw everything
    screen.fill(BLUE)
    
    # Draw clouds
    for cloud in clouds:
        pygame.draw.ellipse(screen, WHITE, (cloud[0], cloud[1], cloud[2], cloud[2]//2))
        pygame.draw.ellipse(screen, WHITE, (cloud[0] + cloud[2]//4, cloud[1] - cloud[2]//4, cloud[2]//2, cloud[2]//2))
    
    # Draw grass
    for blade in grass_blades:
        # Draw each blade as a line with slight random variation
        end_x = blade[0] + random.uniform(-2, 2)  # Slight x variation for wave effect
        pygame.draw.line(screen, GRASS_GREEN, 
                        (blade[0], HEIGHT), 
                        (end_x, blade[1]), 
                        2)  # Width of 2 pixels

    # Draw particles
    for particle in particles:
        alpha = 255 * (1 - particle.age/particle.lifetime)
        particle_surface = pygame.Surface((particle.size, particle.size), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, (*particle.color, int(alpha)), 
                         (particle.size//2, particle.size//2), particle.size//2)
        screen.blit(particle_surface, (particle.x - particle.size//2, particle.y - particle.size//2))

    # Draw bullets with glow effect
    for bullet in bullets:
        # Glow
        glow_size = bullet_size * 2
        glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (ORANGE[0], ORANGE[1], ORANGE[2], 100),
                         (glow_size//2, glow_size//2), glow_size//2)
        screen.blit(glow_surface, (bullet[0] - glow_size//4, bullet[1] - glow_size//4))
        # Bullet
        pygame.draw.circle(screen, ORANGE, (bullet[0] + bullet_size//2, bullet[1] + bullet_size//2), bullet_size//2)
    
    # Draw enemy with better design
    enemy_center = (enemy_x + enemy_size//2, enemy_y + enemy_size//2)
    # Enemy body (rounded rectangle effect)
    pygame.draw.circle(screen, RED, (enemy_x + enemy_size//2, enemy_y + enemy_size//2), enemy_size//2)
    # Angry eyes
    eye_color = BLACK
    eye_size = 6
    pygame.draw.line(screen, eye_color, (enemy_center[0] - 10, enemy_center[1] - 5),
                    (enemy_center[0] - 5, enemy_center[1] + 5), 3)
    pygame.draw.line(screen, eye_color, (enemy_center[0] - 10, enemy_center[1] + 5),
                    (enemy_center[0] - 5, enemy_center[1] - 5), 3)
    pygame.draw.line(screen, eye_color, (enemy_center[0] + 5, enemy_center[1] - 5),
                    (enemy_center[0] + 10, enemy_center[1] + 5), 3)
    pygame.draw.line(screen, eye_color, (enemy_center[0] + 5, enemy_center[1] + 5),
                    (enemy_center[0] + 10, enemy_center[1] - 5), 3)
    
    # Draw player with better design
    # Body
    pygame.draw.circle(screen, WHITE, (player_x + player_size//2, player_y + player_size//2), player_size//2)
    # Eyes
    eye_color = BLACK
    eye_size = 8
    pygame.draw.circle(screen, eye_color, (player_x + player_size//3, player_y + player_size//2), eye_size)
    pygame.draw.circle(screen, eye_color, (player_x + 2*player_size//3, player_y + player_size//2), eye_size)
    # Pupils
    pupil_color = WHITE
    pupil_size = 3
    pygame.draw.circle(screen, pupil_color, (player_x + player_size//3, player_y + player_size//2), pupil_size)
    pygame.draw.circle(screen, pupil_color, (player_x + 2*player_size//3, player_y + player_size//2), pupil_size)
    
    # Draw stars with better design
    for star in stars:
        # Star glow
        glow_size = star[2] * 1.5
        glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (YELLOW[0], YELLOW[1], YELLOW[2], 100),
                         (glow_size//2, glow_size//2), glow_size//2)
        screen.blit(glow_surface, (star[0] - glow_size//4, star[1] - glow_size//4))
        
        # Star points
        center = (star[0] + star[2]//2, star[1] + star[2]//2)
        points = []
        for i in range(10):  # 5-pointed star
            angle = math.pi * 2 * i / 10
            radius = star[2]//2 if i % 2 == 0 else star[2]//4
            points.append((
                center[0] + math.cos(angle) * radius,
                center[1] + math.sin(angle) * radius
            ))
        pygame.draw.polygon(screen, YELLOW, points)

    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()