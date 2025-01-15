import math
import random
import numpy as np
import pygame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.font.init()
#------------------------------------------------------Background algorithm------
scale = 400.0  # Controls how "zoomed in" the map is


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
    #Generate Perlin noise at (x, y)
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


#generate perlin noise map efficiently using NumPy -vectors-
def generate_perlin_noise(width, height, scale, permutation):
    # Create a grid of coordinates
    x_coords = np.linspace(0, width / scale, width, endpoint=False)
    y_coords = np.linspace(0, height / scale, height, endpoint=False)

    # Create meshgrid of coordinates
    x_grid, y_grid = np.meshgrid(x_coords, y_coords)

    # Vectorized perlin noise generation
    noise_map = np.vectorize(lambda x, y: perlin(x, y, permutation))(x_grid, y_grid)

    # Normalise and scale noise to [0, 255] range
    noise_map = ((noise_map + 1) / 2) * 255
    noise_map = noise_map.astype(np.uint8)  # Convert to integer type for pygame

    # Convert the noise map to a pygame surface
    return pygame.surfarray.make_surface(noise_map)

#-----------------------------------------------------------------------Physics Simulations-------------
class Coulombs():
    def __init__(self, q1, q2, m, x, y):
        # Coulomb's constant
        self.k = 8.99e9  # in N m^2 / C^2
        self.q1 = q1  # Charge 1
        self.q2 = q2  # Charge 2
        self.m = m  # Mass of the particle
        self.t = 0
        self.s = 0
        self.x = x
        self.y = y

    def set_q1(self, q1):
        if isinstance(q1, (int, float)):  # Check if the input is a number
            self.q1 = q1
        else:
            raise ValueError("Charge q1 must be a number")

    def set_q2(self, q2):
        if isinstance(q2, (int, float)):  # Check if the input is a number
            self.q2 = q2
        else:
            raise ValueError("Charge q2 must be a number")

    def set_m(self, m):
        if isinstance(m, (int, float)) and m > 0:  # Ensure mass is a positive number
            self.m = m
        else:
            raise ValueError("Mass must be a positive number")

    def calculate_force(self):
        if self.x == 674 and self.y == 538:
            x, y = 675, 539
        else:
            x, y = self.x, self.y
        # Calculate force using Coulomb's Law
        r = math.sqrt((x - 674) ** 2 + (y - 538) ** 2)
        qt = self.q1 * self.q2  # Product of charges
        denom = self.k * (r ** 2)  # Coulomb's constant and squared distance
        force = (qt / denom) * 100000000  # Force
        print("Force = ", force)
        return force

    def calculate_displacement(self):
        self.t += 0.1  # Increase time by a small step
        acceleration = self.calculate_acceleration()  # Calculate acceleration
        self.s = 0.5 * acceleration * (self.t ** 2)  # Displacement using kinematic equation

    def calculate_acceleration(self):
        # Calculate the force
        force = self.calculate_force()
        acceleration = force / self.m  # F = ma => a = F/m
        return acceleration

    def calculate_angle(self):
        # Calculate the displacement from the central point (674, 538)
        delta_x = self.x - 674  # Displacement in the x-direction
        delta_y = self.y - 538  # Displacement in the y-direction

        # Use math.atan2 to calculate the angle in radians
        angle = math.atan2(delta_y, delta_x)  # atan2 automatically handles all quadrants

        return angle

    def repelcheck(self):
        # sets a boolean value based on positive or negative charge
        if self.q1 > 0:
            q1posi = True
        else:
            q1posi = False

        if self.q2 > 0:
            q2posi = True
        else:
            q2posi = False

        if q1posi == False and q2posi == False:
            repel = True
            print("repel 1")
        elif q1posi == True and q2posi == True:
            repel = True
            print("repel 2")
        else:
            repel = False
            print("repel false")

        return repel

    def direction(self):
        direction = self.repelcheck()
        if direction == True:
            return (True)
        elif direction == False:
            return (False)

    def repulsion(self):
        # Update position based on displacement (s)
        self.calculate_displacement()  # Update displacement

        # Calculate the angle in radians
        angle = self.calculate_angle()
        # Determine direction of movement (attraction or repulsion)

        # Move the particle away from the center (along the line connecting the charges)
        self.x += self.s * math.cos(angle)
        self.y += self.s * math.sin(angle)
        print("repel 1")

    def attraction(self):
        # Update position based on displacement (s)
        self.calculate_displacement()

        angle = self.calculate_angle()

        print(f"Moving towards center. Current x: {self.x}, y: {self.y}")
        self.x += self.s * math.cos(angle)
        self.y += self.s * math.sin(angle)
        print(f"Updated x: {self.x}, y: {self.y}")
        print("repel false")

    def draw(self, screen):
        # Scale x and y to fit in the Pygame window
        # Draw the particle as a circle
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 10)  # Red particle


class Waves():
    def __init__(self, amp, wavlen, phase1, angfreq, tsf, phase2):
        self.amp = amp
        self.wavlen = wavlen
        self.phase1 = phase1  # Phase should be in radians
        self.phase2 = phase2
        self.angfreq = angfreq  # Angular frequency should be in radians per second
        self.time = 0.1  # Starting time in seconds
        self.points = []
        self.tsf = tsf  # time scale factor

    def set_amp(self, amp):
        if isinstance(amp, (int, float)):  # Check if the input is a number
            self.amp = amp
        else:
            raise ValueError("Amplitude must be a number")

    def set_wavnum(self, wavlen):
        if isinstance(wavlen, (int, float)):  # Check if the input is a number
            self.wavlen = wavlen
        else:
            raise ValueError("Wave number must be a number")

    def set_phase1(self, phase):
        if isinstance(phase, (int, float)):  # Phase should be in radians
            self.phase1 = phase
        else:
            raise ValueError("Phase must be a number (radians)")

    def set_phase2(self, phase):
        if isinstance(phase, (int, float)):  # Phase should be in radians
            self.phase2 = phase
        else:
            raise ValueError("Phase must be a number (radians)")

    def set_angfreq(self, angfreq):
        if isinstance(angfreq, (int, float)):  # Angular frequency should be in radians per second
            self.angfreq = angfreq
        else:
            raise ValueError("Angular frequency must be a number (radians per second)")

    def set_tsf(self, tsf):
        if isinstance(tsf, (int, float)):  # Check if the input is a number
            self.tsf = tsf
        else:
            raise ValueError("Wave number must be a number")

    def equation(self, x, phase):
        if self.wavlen != 0:
            wavnum = (2 * math.pi) / self.wavlen
        else:
            wavnum = 0
        p1 = wavnum * x  # Wave number times position
        p2 = self.angfreq * self.time  # Angular frequency times time
        p3 = p1 - p2 + phase  # Complete phase term
        y = self.amp * math.cos(p3)  # Calculate y using cosine (in radians)
        self.time += self.tsf  # Increment time slightly for each calculation
        return y

    def wave_points(self, phase):
        points = []  # List to store the points for the wave
        if phase == True:
            for each in range(240, 1199):  # Iterate over the x-values (positions)
                y = (self.equation(each, self.phase1) + 550)  # Get the wave value, shift it by 550 for visibility
                points.append((each, y))  # Add the point (x, y) to the list
            return points
        elif phase == False:
            for each in range(240, 1199):  # Iterate over the x-values (positions)
                y = (self.equation(each, self.phase2) + 550)  # Get the wave value, shift it by 550 for visibility
                points.append((each, y))  # Add the point (x, y) to the list
            return points

    def wave_draw(self):
        points1 = self.wave_points(True)  # Get the points for the wave
        points2 = self.wave_points(False)
        pygame.draw.lines(screen, blue, False, points1, 3)  # Draw the wave on the screen using pygame
        pygame.draw.lines(screen, red, False, points2, 3)


class Stokes_Law():
    def __init__(self, radius,p1,p2,vis,centr,x,y,colour):
        self.radius = radius
        self.p1 = p1 # density of particle
        self.p2 = p2 # density of solvent
        self.g = 9.81 # gravitational constant
        self.vis = vis # viscosity of solvent
        self.centr = centr # centrifuge influences how much gravity is applied
        self.x = x
        self.y = y
        self.colour = colour


    def set_rad(self, radius):
        if isinstance(radius, (int, float)):
            self.radius = radius
        else:
            raise ValueError("Radius must be a number")

    def set_p1(self, p1):
        if isinstance(p1, (int, float)):
            self.p1 = p1
        else:
            raise ValueError("Particle Density must be a number")

    def set_p2(self, p2):
        if isinstance(p2, (int, float)):
            self.p2 = p2
        else:
            raise ValueError("Density of solvent must be a number (radians)")

    def set_viscosity(self, vis):
        if isinstance(vis, (int, float)):
            self.vis = vis
        else:
            raise ValueError("Viscosity must be a number (radians per second)")

    def set_centrifuge(self, centr):
        if isinstance(centr, (int, float)):
            self.centr = centr
        else:
            raise ValueError("Centrifugal force must be a number")

    def equation(self):
        d = (2*self.radius)**2
        pt = self.p1 - self.p2
        g = self.centr * self.g
        numerator = d * pt * g
        denom = 180000 * self.vis
        velocity = numerator/denom
        print(velocity)
        self.y += velocity


    def draw_particle(self,screen):

        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.radius)





swidth, sheight = 1200, 1000

x_mid = swidth / 2
y_mid = sheight / 2
pygame.display.set_caption("Physics simulations")

screen = pygame.display.set_mode((swidth, sheight))

dgrey = (47, 54, 52)
grey = (100, 100, 100)
black = (17, 18, 18)
white = (255, 255, 255)
green = (0, 200, 0)
red = (200, 0, 0)
background_blue = (0, 5, 86)
blue = (0, 117, 200)
orange = (255, 127, 0)
purple = (76, 0, 153)


def hexagon(x, y, scale):  # creates a hexagonal button
    multi1 = scale * 10  # scales the size of the hexagon
    multi2 = scale * 5
    multi3 = scale * 11
    p1 = (x + multi1, y + multi2)  # calculates the six points of the hexagon
    p2 = (x + multi1, y - multi2)
    p3 = (x, y - multi3)
    p4 = (x - multi1, y - multi2)
    p5 = (x - multi1, y + multi2)
    p6 = (x, y + multi3)
    points = [p1, p2, p3, p4, p5, p6]  # adds the points to a list and returns the list
    return points


def poly_draw(colour1, colour2, points, ):  # takes a colour for each polygon and the list of points
    pygame.draw.polygon(screen, colour1, points, 0)
    pygame.draw.polygon(screen, colour2, points, 4)


def poly_rect(points):
    min_x = min(points, key=lambda x: x[0])[0]
    max_x = max(points, key=lambda x: x[0])[0]
    min_y = min(points, key=lambda x: x[1])[1]
    max_y = max(points, key=lambda x: x[1])[1]
    button_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
    return button_rect


def rectangle(width, height, x, y, centre):
    w = width * swidth / 10
    h = height * sheight / 10
    x = x * swidth / 10
    y = y * sheight / 10
    if centre == True:
        x = x_mid - (w / 2)
    return (x, y, w, h)


def pos_check(button):
    return button.collidepoint(pygame.mouse.get_pos())


def draw_slider(screen, x, y, width, height, min, max, step):
    slider = Slider(screen, x, y, width, height, min=min, max=max, step=step)
    return (slider)


def draw_output(screen, x, y, width, height):
    output = TextBox(screen, x, y, width, height, fontSize=20)
    output.disable()
    return (output)


def format_value(label, value, max_len=4):
    # Format the value to at most 4 characters, including the decimal point
    formatted_value = f"{value:.3f}"  # Round to 3 decimal places
    if len(formatted_value) > max_len:  # Check if length exceeds 4 characters
        formatted_value = formatted_value[:max_len]  # Trim the string to 4 characters

    # Add the label to the formatted value
    return f"{label} {formatted_value}"

#-----------------------------------------------------------------------------labels----
font = pygame.font.Font('freesansbold.ttf', 32)
coulombstitle = font.render("Coulomb's Law", True, white)
coulombstitleRect = coulombstitle.get_rect() 
# set the center of the rectangular object.
coulombstitleRect.center = (600,50)
wavestitle = font.render('Wave Equation', True, white)
wavestitleRect = wavestitle.get_rect() 
# set the center of the rectangular object.
wavestitleRect.center = (600,50)
stokestitle = font.render("Stoke's Law", True, white)
stokestitleRect = stokestitle.get_rect() 
# set the center of the rectangular object.
stokestitleRect.center = (600,50)

title = font.render("Simulations", True, white)
titleRect = title.get_rect() 
# set the center of the rectangular object.
titleRect.center = (600,50)

back = font.render("Back", True, red)
backRect = back.get_rect() 
# set the center of the rectangular object.
backRect.center = (80,45)


coulombsbutton = font.render("Coulomb's Law", True, white)
coulombsbuttonRect = coulombsbutton.get_rect() 
# set the center of the rectangular object.
coulombsbuttonRect.center = (375,350)
wavesbutton = font.render('Wave Equation', True, white)
wavesbuttonRect = wavesbutton.get_rect() 
# set the center of the rectangular object.
wavesbuttonRect.center = (800,350)
stokesbutton = font.render("Stoke's Law", True, white)
stokesbuttonRect = stokesbutton.get_rect() 
# set the center of the rectangular object.
stokesbuttonRect.center = (575,675)
#-----------------------------------------------------------------
stokes_particles = []
running = True
current_screen = ["menu"]
clicked = False
toggle = False
sim_run = False
clock = pygame.time.Clock()
# Initialize permutation table
permutation = generate_permutation()
noise_map = generate_perlin_noise(swidth, sheight, scale, permutation)
map = pygame.transform.scale(noise_map, (noise_map.get_height(), sheight))
# Create a clock object to manage FPS

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = event.pos

    pygame.display.update()
    screen.fill(black)
    if current_screen[-1] != "ipsum":  # draws the bar at the top of the screen at all points
        screen.blit(map, (0, 0))
        header = pygame.draw.rect(screen, dgrey, rectangle(10, 1, 0, 0, False))
        # creates the bar at the top of the screen
        title_box = pygame.draw.rect(screen, grey, rectangle(2, 0.45, 4, 0.25, True))
        # creates the title box at the top of the screen
        if current_screen[-1] != "menu":
            back_button = pygame.draw.rect(screen, purple, rectangle(1, 0.4, 0.25, 0.25, False))
            screen.blit(back,backRect)
            # creates the back button
            if pos_check(back_button):
                back_button = pygame.draw.rect(screen, orange, rectangle(1, 0.4, 0.25, 0.25, False))
                screen.blit(back,backRect)
                # changes the colour of the back button when hovered
                if event.type == pygame.MOUSEBUTTONDOWN and len(current_screen) > 1:
                    current_screen.pop()
                    stokes_particles.clear()
                    sim_run = False

    if current_screen[-1] == "menu":  # defines the polygons on the menu screen-----------------------------------
        clicked = True
        screen.blit(title,titleRect)
        # Charge Button
        chrg_button_points = hexagon(380, 350, 20)  # calculates each of the points for the hexagon
        chrg_button = poly_draw(purple, blue, chrg_button_points)  # draws the hexagon on screen with outline
        chrg_rect = poly_rect(chrg_button_points)  # creates the rect around the polygon for it to be interactable
        screen.blit(coulombsbutton,coulombsbuttonRect)
        # Mass Button
        stokes_button_points = hexagon(580, 670, 20)
        stokes_button = poly_draw(purple, blue, stokes_button_points)
        stokes_rect = poly_rect(stokes_button_points)
        screen.blit(stokesbutton,stokesbuttonRect)
        # Wave Button
        wave_button_points = hexagon(780, 350, 20)
        wave_button = poly_draw(purple, blue, wave_button_points)
        wave_rect = poly_rect(wave_button_points)
        screen.blit(wavesbutton,wavesbuttonRect)

        if chrg_rect.collidepoint(pygame.mouse.get_pos()):
            chrg_button = poly_draw(orange, blue, chrg_button_points)
            screen.blit(coulombsbutton,coulombsbuttonRect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_screen.append("charge_sim")

        if stokes_rect.collidepoint(pygame.mouse.get_pos()):
            mass_button = poly_draw(orange, blue, stokes_button_points)
            screen.blit(stokesbutton,stokesbuttonRect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_screen.append("Stokes Law")

        if wave_rect.collidepoint(pygame.mouse.get_pos()):
            wave_button = poly_draw(orange, blue, wave_button_points)
            screen.blit(wavesbutton,wavesbuttonRect)
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_screen.append("wave_sim")

    if current_screen[-1] == "charge_sim":  # ---------------------------------------------------------------
        sidebar = pygame.draw.rect(screen, red, rectangle(2, 9, 0, 1, False))
        backgrnd1 = pygame.draw.rect(screen, black, rectangle(10, 10, 2, 1, False))
        screen.blit(coulombstitle,coulombstitleRect)
        if clicked == True:
            slider1 = draw_slider(screen, 50, 458, 150, 20, -100, 100, 1)
            output1 = draw_output(screen, 25, 400, 150, 40)
            slider2 = draw_slider(screen, 50, 558, 150, 20, -100, 100, 1)
            output2 = draw_output(screen, 25, 500, 150, 40)
            slider3 = draw_slider(screen, 50, 658, 150, 20, 1, 100, 1)
            output3 = draw_output(screen, 25, 600, 150, 40)
            slider4 = draw_slider(screen, 50, 758, 150, 20, -3.14, 3.14, 0.1)
            output4 = draw_output(screen, 25, 700, 210, 40)
            slider5 = draw_slider(screen, 50, 358, 150, 20, 0.0000001, 0.0001, 0.0000001)
            output5 = draw_output(screen, 25, 300, 150, 40)
            slider6 = draw_slider(screen, 50, 758, 150, 20, -4, 4, 0.1)
            output6 = draw_output(screen, 25, 700, 200, 40)
            clicked = False
        slider1.listen(events)
        output1.setText(format_value("Charge 1:", slider1.getValue()))
        slider2.listen(events)
        output2.setText(format_value("Charge 2:", slider2.getValue()))
        slider3.listen(events)
        output3.setText(format_value("Mass:", slider3.getValue()))
        slider4.hide()
        slider5.hide()
        output4.hide()
        output5.hide()
        slider6.hide()
        output6.hide()
        pygame.draw.circle(screen, (0, 0, 255), (674, 538), 10)
        if backgrnd1.collidepoint(pygame.mouse.get_pos()):
            mousex, mousey = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                instance1 = Coulombs(slider1.getValue(), slider2.getValue(), slider3.getValue(), mousex, mousey)
                sim_run = True
        if sim_run == True:
            # print("sim")
            direction = instance1.direction()
            instance1.draw(screen)
            instance1.set_q1(slider1.getValue())
            instance1.set_q2(slider2.getValue())
            instance1.set_m(slider3.getValue())
            if direction == True:
                instance1.repulsion()
            elif direction == False:
                instance1.attraction()

    if current_screen[-1] == "Stokes Law":  # -------------------------------------------------------------------
        sidebar = pygame.draw.rect(screen, purple, rectangle(2, 9, 0, 1, False))
        backgrnd1 = pygame.draw.rect(screen, black, rectangle(10, 10, 2, 1, False))
        screen.blit(stokestitle,stokestitleRect)
        if clicked == True:
            slider1 = draw_slider(screen, 50, 458, 150, 20, 1, 20, 1)
            output1 = draw_output(screen, 25, 400, 150, 40)
            slider2 = draw_slider(screen, 50, 558, 150, 20, 500, 1500, 50, )
            output2 = draw_output(screen, 25, 500, 210, 40)
            slider3 = draw_slider(screen, 50, 658, 150, 20, 500, 1500, 50)
            output3 = draw_output(screen, 25, 600, 210, 40)
            slider4 = draw_slider(screen, 50, 758, 150, 20, 1, 100, 1)
            output4 = draw_output(screen, 25, 700, 150, 40)
            slider5 = draw_slider(screen, 50, 358, 150, 20, 1, 40, 1)
            output5 = draw_output(screen, 25, 300, 200, 40)
            slider6 = draw_slider(screen, 50, 758, 150, 20, 1, 10, 1)
            output6 = draw_output(screen, 25, 700, 200, 40)
            clicked = False
        slider1.listen(events)
        output1.setText(format_value("Radius:", slider1.getValue()))
        slider2.listen(events)
        output2.setText(format_value("Density of Particle:", slider2.getValue()))
        slider3.listen(events)
        output3.setText(format_value("Density of Solvent:", slider3.getValue()))
        slider4.listen(events)
        output4.setText(format_value("Viscosity:", slider4.getValue()))
        slider5.listen(events)
        output5.setText(format_value("Centrifugal Force:", slider5.getValue()))
        slider6.hide()
        output6.hide()
        if backgrnd1.collidepoint(pygame.mouse.get_pos()):
            mousex, mousey = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(1,5):
                    r = random.randint(138,240)
                    g = random.randint(109,200)
                    b = random.randint(13,58)
                    colour = (r,g,b)
                    x = random.randint(250,1190)
                    y = random.randint(105,990)
                    stokes_particles.append(Stokes_Law(slider1.getValue(), slider2.getValue(), slider3.getValue(),slider4.getValue(),slider5.getValue(), x, y,colour))
                    sim_run = True
        if sim_run == True:
            for each in stokes_particles:
                each.set_rad(slider1.getValue())
                each.set_p1(slider2.getValue())
                each.set_p2(slider3.getValue())
                each.set_viscosity(slider4.getValue())
                each.set_centrifuge(slider5.getValue())
                each.equation()
                each.draw_particle(screen)





    if current_screen[-1] == "wave_sim":  # --------------------------------------------------------------------
        sidebar = pygame.draw.rect(screen, purple, rectangle(2, 9, 0, 1, False))
        backgrnd1 = pygame.draw.rect(screen, black, rectangle(10, 10, 2, 1, False))
        screen.blit(wavestitle,wavestitleRect)
        if clicked == True:
            slider1 = draw_slider(screen, 50, 458, 150, 20, -300, 300, 1)
            output1 = draw_output(screen, 25, 400, 150, 40)
            slider2 = draw_slider(screen, 50, 558, 150, 20, -4, 4, 0.1, )
            output2 = draw_output(screen, 25, 500, 150, 40)
            slider3 = draw_slider(screen, 50, 658, 150, 20, -300, 300, 1)
            output3 = draw_output(screen, 25, 600, 200, 40)
            slider4 = draw_slider(screen, 50, 858, 150, 20, -3.14, 3.14, 0.1)
            output4 = draw_output(screen, 25, 800, 210, 40)
            slider5 = draw_slider(screen, 50, 358, 150, 20, 0.0000001, 0.0001, 0.0000001)
            output5 = draw_output(screen, 25, 300, 150, 40)
            slider6 = draw_slider(screen, 50, 758, 150, 20, -4, 4, 0.1)
            output6 = draw_output(screen, 25, 700, 200, 40)
            clicked = False
        if backgrnd1.collidepoint(pygame.mouse.get_pos()):
            mousex, mousey = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                wave = Waves(slider1.getValue(), slider2.getValue(), slider3.getValue(), slider4.getValue(),
                             slider5.getValue(), slider6.getValue())
                sim_run = True
        slider1.listen(events)
        output1.setText(format_value("Amplitude:", slider1.getValue()))
        slider2.listen(events)
        output2.setText(format_value("Phase1:", slider2.getValue()))
        slider3.listen(events)
        output3.setText(format_value("Wavelength:", slider3.getValue()))
        slider4.listen(events)
        output4.setText(format_value("Angular Frequency:", slider4.getValue()))
        slider5.listen(events)
        output5.setText(format_value("Time Scale:", slider5.getValue()))
        slider6.listen(events)
        output6.setText(format_value("Phase2:", slider6.getValue()))

        if sim_run == True:
            wave.wave_draw()
            wave.set_amp(slider1.getValue())
            wave.set_phase1(slider2.getValue())
            wave.set_wavnum(slider3.getValue())
            wave.set_angfreq(slider4.getValue())
            wave.set_tsf(slider5.getValue())
            wave.set_phase2(slider6.getValue())


    if current_screen[-1] == "Stokes Law" or current_screen[-1] == "charge_sim" or current_screen[-1] == "wave_sim":
        pygame_widgets.update(events)

    pygame.display.update()
