import pygame
import random
import math

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
    # Determine grid cell coordinates
    X = int(x) & 255
    Y = int(y) & 255

    # Relative coordinates inside grid cell
    xf = x - int(x)
    yf = y - int(y)

    # Fade the coordinates to smooth the results
    u = fade(xf)
    v = fade(yf)

    # Hash the corners
    aa = permutation[permutation[X] + Y]
    ab = permutation[permutation[X] + Y + 1]
    ba = permutation[permutation[X + 1] + Y]
    bb = permutation[permutation[X + 1] + Y + 1]

    # Interpolate
    x1 = lerp(grad(aa, xf, yf), grad(ba, xf - 1, yf), u)
    x2 = lerp(grad(ab, xf, yf - 1), grad(bb, xf - 1, yf - 1), u)
    return lerp(x1, x2, v)

# Generate a permutation table (this is a random pattern used to shuffle the gradient vectors)
def generate_permutation():
    p = list(range(256))
    random.shuffle(p)
    p = p * 2  # Double the permutation table
    return p

# Function to generate Perlin noise map
def generate_perlin_noise(width, height, scale, permutation, camera_x, camera_y):
    noise_map = pygame.Surface((width, height))  # Create a surface for the noise map
    for y in range(height):
        for x in range(width):
            nx = (x + camera_x) / scale
            ny = (y + camera_y) / scale
            noise_value = perlin(nx, ny, permutation)
            noise_value = (noise_value + 1) / 2  # Scale to the range [0, 1]
            noise_value = min(1, max(0, noise_value))  # Clamp between 0 and 1

            # Map the noise value to a color
            color_value = int(noise_value * 255)  # Map from [0,1] to [0, 255]
            color = (color_value, color_value, color_value)  # RGB color (gray scale)

            # Set the pixel color on the surface
            noise_map.set_at((x, y), color)

    return noise_map

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

    # Display the background
    pygame.display.update()

    # Event handling (to close the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Quit Pygame
pygame.quit()
