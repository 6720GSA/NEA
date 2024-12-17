import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Static Perlin Noise Background")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Perlin noise parameters
scale = 100.0  # Controls how "zoomed in" the noise is
octaves = 6  # Number of iterations (higher for more detail)
persistence = 0.5  # How much influence each octave has
lacunarity = 2.0  # Frequency multiplier between octaves


# Gradient vector for Perlin noise
def grad(hash, x, y):
    #Calculate gradient based on hash value
    h = hash & 15
    u = x if h < 8 else y
    v = y if h < 4 else x
    return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)


# Fade function for smoothing the Perlin noise curve
def fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)


# Linear interpolation
def lerp(a, b, t):
    return a + t * (b - a)


# Perlin Noise Function
def perlin(x, y, permutation):
    """Generate Perlin noise at (x, y)"""
    X = int(x) & 255
    Y = int(y) & 255

    xf = x - int(x)
    yf = y - int(y)

    u = fade(xf)
    v = fade(yf)

    aa = permutation[permutation[X] + Y]
    ab = permutation[permutation[X] + Y + 1]
    ba = permutation[permutation[X + 1] + Y]
    bb = permutation[permutation[X + 1] + Y + 1]

    x1 = lerp(grad(aa, xf, yf), grad(ba, xf - 1, yf), u)
    x2 = lerp(grad(ab, xf, yf - 1), grad(bb, xf - 1, yf - 1), u)
    return lerp(x1, x2, v)


# Generate a permutation table (this is a random pattern used to shuffle the gradient vectors)
def generate_permutation():
    p = list(range(256))
    random.shuffle(p)
    p = p * 2  # Double the permutation table
    return p


# Function to generate Perlin noise map efficiently using NumPy (vectorized)
def generate_perlin_noise(width, height, scale, permutation):
    # Create a grid of coordinates for the noise generation
    x_coords = np.linspace(0, width / scale, width, endpoint=False)
    y_coords = np.linspace(0, height / scale, height, endpoint=False)

    # Create meshgrid of coordinates
    x_grid, y_grid = np.meshgrid(x_coords, y_coords)

    # Vectorized Perlin noise generation
    noise_map = np.vectorize(lambda x, y: perlin(x, y, permutation))(x_grid, y_grid)

    # Normalize and scale noise to [0, 255] range
    noise_map = ((noise_map + 1) / 2) * 255  # Normalize to [0, 1] and then to [0, 255]
    noise_map = noise_map.astype(np.uint8)  # Convert to integer type for Pygame

    # Convert the noise map to a Pygame surface
    return pygame.surfarray.make_surface(noise_map)

def stretchmap(image, newWidth):
    return pygame.transform.scale(image, (image.get_height(), newWidth))

# Initialize permutation table
permutation = generate_permutation()

# Create a clock object to manage FPS
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Main loop
running = True
while running:
    screen.fill(BLACK)  # Clear the screen with black

    # Generate the Perlin noise for the background (static, no drift)
    noise_map = generate_perlin_noise(width, height, scale, permutation)
    map = stretchmap(noise_map,1000)
    # Blit the noise map to the screen
    screen.blit(map, (0, 0))

    # Display FPS
    fps_text = font.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    screen.blit(fps_text, (10, 10))

    # Display the background
    pygame.display.update()

    # Event handling (to close the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the FPS counter
    clock.tick(60)  # Limit the frame rate to 60 FPS

# Quit Pygame
pygame.quit()
