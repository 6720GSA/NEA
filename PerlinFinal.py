import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Set up the screen
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pulsing Perlin Noise Background")

# Perlin noise parameters
scale = 100.0  # Controls how "zoomed in" the noise is
octaves = 6     # Number of iterations (higher for more detail)
persistence = 0.5  # How much influence each octave has
lacunarity = 2.0  # Frequency multiplier between octaves

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

# Function to generate Perlin noise map with color
def generate_perlin_noise(width, height, scale, permutation, time_factor):
    noise_map = pygame.Surface((width, height))  # Create a surface for the noise map
    for y in range(height):
        for x in range(width):
            nx = x / scale  # No camera movement, fixed generation
            ny = y / scale
            noise_value = perlin(nx, ny, permutation)
            noise_value = (noise_value + 1) / 2  # Scale to the range [0, 1]
            noise_value = min(1, max(0, noise_value))  # Clamp between 0 and 1

            # Map the noise value to a color (using the pulsing color gradient)
            color = get_pulsing_color_from_noise(noise_value, time_factor)

            # Set the pixel color on the surface
            noise_map.set_at((x, y), color)

    return noise_map

# Function to map Perlin noise value to a pulsing color (from magenta to blue)
def get_pulsing_color_from_noise(value, time_factor):
    """Map a Perlin noise value (0 to 1) to a color (from magenta to blue) with pulsing effect"""
    
    # Magenta: #C33764 (RGB: 195, 55, 100)
    # Blue: #1D2671 (RGB: 29, 38, 113)

    # Pulsing effect: Use sine wave to create an oscillating factor
    pulse_factor = 0.5 * math.sin(time_factor) + 0.5  # This oscillates between 0 and 1

    # Interpolate between the colors using the pulsing factor
    r = int((29 - 195) * value * pulse_factor + 195)  # Interpolation for red (from 195 to 29)
    g = int((38 - 55) * value * pulse_factor + 55)    # Interpolation for green (from 55 to 38)
    b = int((113 - 100) * value * pulse_factor + 100) # Interpolation for blue (from 100 to 113)

    return (r, g, b)

# Initialize permutation table
permutation = generate_permutation()

# Main loop
running = True
clock = pygame.time.Clock()
time_factor = 0  # Variable to control the pulsing speed

while running:
    screen.fill((0, 0, 0))  # Clear the screen with black

    # Generate the Perlin noise for the background with the pulsing effect
    noise_map = generate_perlin_noise(width, height, scale, permutation, time_factor)

    # Blit the noise map to the screen
    screen.blit(noise_map, (0, 0))

    # Update the time factor for pulsing effect (time-based)
    time_factor += 0.1  # Controls the speed of the pulsing

    # Display the background
    pygame.display.update()

    # Event handling (to close the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Limit FPS to make pulsing smooth
    clock.tick(60)

# Quit Pygame
pygame.quit()
