// Initialize canvas and context
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

// Set up the display
const WIDTH = 800;
const HEIGHT = 600;
canvas.width = WIDTH;
canvas.height = HEIGHT;

// Colors
const WHITE = 'rgb(255, 255, 255)';
const BLUE = 'rgb(100, 149, 237)';
const YELLOW = 'rgb(255, 255, 0)';
const RED = 'rgb(255, 0, 0)';
const BLACK = 'rgb(0, 0, 0)';
const ORANGE = 'rgb(255, 165, 0)';
const GRASS_GREEN = 'rgb(34, 139, 34)';

// Game state
let score = 0;
let running = true;

// Visual effects
class Particle {
    constructor(x, y, color, size, speedX, speedY, lifetime) {
        this.x = x;
        this.y = y;
        this.color = color;
        this.size = size;
        this.speedX = speedX;
        this.speedY = speedY;
        this.lifetime = lifetime;
        this.age = 0;
    }
}
let particles = [];

// Background elements
let clouds = Array(5).fill().map(() => ({
    x: Math.random() * WIDTH,
    y: Math.random() * (HEIGHT / 2),
    size: 50 + Math.random() * 50
}));

// Grass properties
const GRASS_HEIGHT = 20;
const GRASS_SPACING = 5;
let grassBlades = [];
for (let x = 0; x < WIDTH; x += GRASS_SPACING) {
    const heightVariation = Math.random() * 10 - 5;
    grassBlades.push([x, HEIGHT - GRASS_HEIGHT + heightVariation]);
}

// Player properties
const playerSize = 40;
let playerX = WIDTH / 2;
let playerY = HEIGHT - playerSize;
const playerSpeed = 5;
const playerJump = -5;  // Changed from -15 to -10 to make jumps lower
let playerVelocity = 0;
const gravity = 0.8;

// Bullet properties
let bullets = [];
const bulletSpeed = 10;
const bulletSize = 8;

// Enemy properties
const enemySize = 30;
let enemyX = Math.random() * (WIDTH - enemySize);
let enemyY = Math.random() * (HEIGHT - enemySize);
const enemySpeed = 3;
let enemyDirection = Math.random() < 0.5 ? -1 : 1;

// Star properties
const starSize = 20;
let stars = Array(5).fill().map(() => ({
    x: Math.random() * (WIDTH - starSize),
    y: Math.random() * (HEIGHT / 2),
    size: starSize
}));

// Input handling
const keys = {
    w: false,
    a: false,
    d: false
};

document.addEventListener('keydown', (e) => {
    if (e.key === 'w') keys.w = true;
    if (e.key === 'a') keys.a = true;
    if (e.key === 'd') keys.d = true;
});

document.addEventListener('keyup', (e) => {
    if (e.key === 'w') keys.w = false;
    if (e.key === 'a') keys.a = false;
    if (e.key === 'd') keys.d = false;
});

canvas.addEventListener('mousedown', (e) => {
    if (e.button === 0) { // Left click
        bullets.push({
            x: playerX + playerSize / 2 - bulletSize / 2,
            y: playerY + playerSize / 2 - bulletSize / 2
        });
    }
});

// Game functions
function updateParticles() {
    particles = particles.filter(particle => {
        particle.x += particle.speedX;
        particle.y += particle.speedY;
        particle.age++;
        return particle.age < particle.lifetime;
    });
}

function updatePlayer() {
    // Move player
    if (keys.a && playerX > 0) playerX -= playerSpeed;
    if (keys.d && playerX < WIDTH - playerSize) playerX += playerSpeed;
    if (keys.w) playerVelocity = playerJump;  // Removed ground check to allow infinite jumps

    // Apply gravity
    playerVelocity += gravity;
    playerY += playerVelocity;

    // Ground collision
    if (playerY > HEIGHT - playerSize) {
        playerY = HEIGHT - playerSize;
        playerVelocity = 0;
    }
}

function updateEnemy() {
    enemyX += enemySpeed * enemyDirection;
    
    if (enemyX <= 0) {
        enemyX = 0;
        enemyDirection = 1;
    } else if (enemyX >= WIDTH - enemySize) {
        enemyX = WIDTH - enemySize;
        enemyDirection = -1;
    }
}

function updateBullets() {
    bullets = bullets.filter(bullet => {
        bullet.x += bulletSpeed;

        // Create particles
        if (Math.random() < 0.3) {
            particles.push(new Particle(
                bullet.x + bulletSize / 2,
                bullet.y + bulletSize / 2,
                ORANGE,
                2 + Math.random() * 2,
                Math.random() * 2 - 1,
                Math.random() * 2 - 1,
                20
            ));
        }

        // Check enemy collision
        if (bullet.x < enemyX + enemySize &&
            bullet.x + bulletSize > enemyX &&
            bullet.y < enemyY + enemySize &&
            bullet.y + bulletSize > enemyY) {
            enemyX = -enemySize;
            enemyY = Math.random() * (HEIGHT - enemySize);
            score += 2;
            return false;
        }

        return bullet.x <= WIDTH;
    });
}

function updateStars() {
    stars = stars.filter(star => {
        if (playerX + playerSize > star.x &&
            playerX < star.x + star.size &&
            playerY + playerSize > star.y &&
            playerY < star.y + star.size) {
            score++;
            return false;
        }
        return true;
    });

    while (stars.length < 5) {
        stars.push({
            x: Math.random() * (WIDTH - starSize),
            y: Math.random() * (HEIGHT / 2),
            size: starSize
        });
    }
}

function updateClouds() {
    clouds.forEach(cloud => {
        cloud.x -= 0.5;
        if (cloud.x + cloud.size < 0) {
            cloud.x = WIDTH;
            cloud.y = Math.random() * (HEIGHT / 2);
        }
    });
}

function checkCollisions() {
    if (playerX < enemyX + enemySize &&
        playerX + playerSize > enemyX &&
        playerY < enemyY + enemySize &&
        playerY + playerSize > enemyY) {
        running = false;
    }
}

// Drawing functions
function drawParticles() {
    particles.forEach(particle => {
        ctx.save();
        ctx.globalAlpha = 1 - (particle.age / particle.lifetime);
        ctx.fillStyle = particle.color;
        ctx.beginPath();
        ctx.arc(particle.x, particle.y, particle.size / 2, 0, Math.PI * 2);
        ctx.fill();
        ctx.restore();
    });
}

function drawPlayer() {
    // Body
    ctx.fillStyle = WHITE;
    ctx.beginPath();
    ctx.arc(playerX + playerSize / 2, playerY + playerSize / 2, playerSize / 2, 0, Math.PI * 2);
    ctx.fill();

    // Eyes
    ctx.fillStyle = BLACK;
    ctx.beginPath();
    ctx.arc(playerX + playerSize / 3, playerY + playerSize / 2, 8, 0, Math.PI * 2);
    ctx.arc(playerX + 2 * playerSize / 3, playerY + playerSize / 2, 8, 0, Math.PI * 2);
    ctx.fill();

    // Pupils
    ctx.fillStyle = WHITE;
    ctx.beginPath();
    ctx.arc(playerX + playerSize / 3, playerY + playerSize / 2, 3, 0, Math.PI * 2);
    ctx.arc(playerX + 2 * playerSize / 3, playerY + playerSize / 2, 3, 0, Math.PI * 2);
    ctx.fill();
}

function drawEnemy() {
    const enemyCenter = {
        x: enemyX + enemySize / 2,
        y: enemyY + enemySize / 2
    };

    // Body
    ctx.fillStyle = RED;
    ctx.beginPath();
    ctx.arc(enemyCenter.x, enemyCenter.y, enemySize / 2, 0, Math.PI * 2);
    ctx.fill();

    // Angry eyes
    ctx.strokeStyle = BLACK;
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(enemyCenter.x - 10, enemyCenter.y - 5);
    ctx.lineTo(enemyCenter.x - 5, enemyCenter.y + 5);
    ctx.moveTo(enemyCenter.x - 10, enemyCenter.y + 5);
    ctx.lineTo(enemyCenter.x - 5, enemyCenter.y - 5);
    ctx.moveTo(enemyCenter.x + 5, enemyCenter.y - 5);
    ctx.lineTo(enemyCenter.x + 10, enemyCenter.y + 5);
    ctx.moveTo(enemyCenter.x + 5, enemyCenter.y + 5);
    ctx.lineTo(enemyCenter.x + 10, enemyCenter.y - 5);
    ctx.stroke();
}

function drawBullets() {
    bullets.forEach(bullet => {
        // Glow
        const gradient = ctx.createRadialGradient(
            bullet.x + bulletSize / 2, bullet.y + bulletSize / 2, 0,
            bullet.x + bulletSize / 2, bullet.y + bulletSize / 2, bulletSize
        );
        gradient.addColorStop(0, ORANGE);
        gradient.addColorStop(1, 'rgba(255, 165, 0, 0)');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(bullet.x + bulletSize / 2, bullet.y + bulletSize / 2, bulletSize, 0, Math.PI * 2);
        ctx.fill();

        // Bullet
        ctx.fillStyle = ORANGE;
        ctx.beginPath();
        ctx.arc(bullet.x + bulletSize / 2, bullet.y + bulletSize / 2, bulletSize / 2, 0, Math.PI * 2);
        ctx.fill();
    });
}

function drawStars() {
    stars.forEach(star => {
        // Star glow
        const gradient = ctx.createRadialGradient(
            star.x + star.size / 2, star.y + star.size / 2, 0,
            star.x + star.size / 2, star.y + star.size / 2, star.size
        );
        gradient.addColorStop(0, YELLOW);
        gradient.addColorStop(1, 'rgba(255, 255, 0, 0)');
        
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.arc(star.x + star.size / 2, star.y + star.size / 2, star.size, 0, Math.PI * 2);
        ctx.fill();

        // Star points
        ctx.fillStyle = YELLOW;
        ctx.beginPath();
        for (let i = 0; i < 10; i++) {
            const angle = Math.PI * 2 * i / 10;
            const radius = i % 2 === 0 ? star.size / 2 : star.size / 4;
            const x = star.x + star.size / 2 + Math.cos(angle) * radius;
            const y = star.y + star.size / 2 + Math.sin(angle) * radius;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.fill();
    });
}

function drawClouds() {
    ctx.fillStyle = WHITE;
    clouds.forEach(cloud => {
        ctx.beginPath();
        ctx.ellipse(cloud.x, cloud.y, cloud.size, cloud.size / 2, 0, 0, Math.PI * 2);
        ctx.fill();
        ctx.beginPath();
        ctx.ellipse(cloud.x + cloud.size / 4, cloud.y - cloud.size / 4, cloud.size / 2, cloud.size / 2, 0, 0, Math.PI * 2);
        ctx.fill();
    });
}

function drawGrass() {
    ctx.strokeStyle = GRASS_GREEN;
    ctx.lineWidth = 2;
    grassBlades.forEach(blade => {
        const endX = blade[0] + (Math.random() * 4 - 2);
        ctx.beginPath();
        ctx.moveTo(blade[0], HEIGHT);
        ctx.lineTo(endX, blade[1]);
        ctx.stroke();
    });
}

function drawScore() {
    ctx.fillStyle = WHITE;
    ctx.font = '36px Arial';
    ctx.fillText(`Score: ${score}`, 10, 40);
}

// Game loop
function gameLoop() {
    if (!running) return;

    // Update game state
    updateParticles();
    updatePlayer();
    updateEnemy();
    updateBullets();
    updateStars();
    updateClouds();
    checkCollisions();

    // Draw everything
    ctx.fillStyle = BLUE;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    
    drawClouds();
    drawGrass();
    drawParticles();
    drawBullets();
    drawStars();
    drawEnemy();
    drawPlayer();
    drawScore();

    requestAnimationFrame(gameLoop);
}

// Start the game
gameLoop();