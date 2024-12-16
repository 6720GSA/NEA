import pygame
import random
import math
import numpy as np

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Drifting Perlin Noise Background")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Perlin noise parameters
scale = 100.0  # Controls how "zoomed in" the noise is
octaves = 6     # Number of iterations (higher for more detail)
persistence = 0.5  # How much influence each octave has
lacunarity = 2.0  # Frequency multiplier between octaves

# Camera position for movement
camera_x = 0.0
camera_y = 0.0
camera_speed = 10  # Speed of the camera movement, adjust this to change drift speed

# Gradient vector for Perlin noise
def grad(hash, x, y):
    """Calculate gradient based on hash value"""
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

# Function to generate Perlin noise map efficiently using NumPy
def generate_perlin_noise(width, height, scale, permutation, camera_x, camera_y):
    # Create a NumPy array to hold noise values
    noise_map = np.zeros((height, width), dtype=np.float32)

    for y in range(height):
        for x in range(width):
            nx = (x + camera_x) / scale
            ny = (y + camera_y) / scale
            noise_value = perlin(nx, ny, permutation)
            noise_map[y, x] = (noise_value + 1) / 2  # Normalize to [0, 1]

    # Convert to RGB
    noise_map = (noise_map * 255).astype(np.uint8)

    # Return the noise map as a pygame surface
    return pygame.surfarray.make_surface(noise_map)

# Initialize permutation table
permutation = generate_permutation()

# Main loop
running = True
while running:
    screen.fill(BLACK)  # Clear the screen with black

    # Generate the Perlin noise for the background with camera movement
    noise_map = generate_perlin_noise(width, height, scale, permutation, camera_x, camera_y)

    # Blit the noise map to the screen
    screen.blit(noise_map, (0, 0))

    # Update the camera position to create the drifting effect
    camera_x += camera_speed  # Adjust this value to control the speed of drift
    camera_y += camera_speed

    # Display the background
    pygame.display.update()

    # Event handling (to close the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
