# https://lampz.tugraz.at/~hadley/physikm/script/waves/wave.en.php

import pygame
import math
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.font.init()


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
        self.repel = True

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
        # Calculate force using Coulomb's Law
        r = math.sqrt((self.x - 674) ** 2 + (self.y - 538) ** 2)
        qt = self.q1 * self.q2  # Product of charges
        denom = self.k * (r ** 2)  # Coulomb's constant and squared distance
        force = (qt / denom) * 100000000  # Force
        print(force)
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
        #sets a boolean value based on positive or negative charge
        if self.q1 > 0:
            q1posi = True
        else:
            q1posi = False

        if self.q2 > 0:
            q2posi = True
        else:
            q2posi = False

        if q1posi == False and q2posi == False:
            self.repel = True
            print("repel 1")
        elif q1posi == True and q2posi == True:
            self.repel = True
            print("repel 2")
        else:
            self.repel = False
            print("repel false")


    def update_position(self):
        # Update position based on displacement (s)
        self.calculate_displacement()  # Update displacement

        # Calculate the angle in radians
        angle = self.calculate_angle()
        # Determine direction of movement (attraction or repulsion)
        if self.q1 > 0:
            q1posi = True
        else:
            q1posi = False

        if self.q2 > 0:
            q2posi = True
        else:
            q2posi = False

        if q1posi == False and q2posi == False:# Charges are the same (repulsive force)
            self.repel = True # Move the particle away from the center (along the line connecting the charges)
            self.x += self.s * math.cos(angle)
            self.y += self.s * math.sin(angle)
            print("repel 1")
        elif q1posi == True and q2posi == True:# Charges are the same (repulsive force)
            self.repel = True # Move the particle away from the center (along the line connecting the charges)
            self.x += self.s * math.cos(angle)
            self.y += self.s * math.sin(angle)
            print("repel 2")
        else:              # Charges are opposite (attractive force)
            self.repel = False # Move the particle towards the center (along the line connecting the charges)
            self.x -= self.s * math.cos(angle)
            self.y -= self.s * math.sin(angle)
            print("repel false")

    def draw(self, screen):
        # Scale x and y to fit in the Pygame window
        print(self.x, self.y)
        # Draw the particle as a circle
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 5)  # Red particle


class Waves():
    def __init__(self, amp, wavnum, phase, angfreq):
        self.amp = amp
        self.wavnum = wavnum
        self.phase = phase
        self.angfreq = angfreq
        self.time = 0.1
        self.points = []

    def set_amp(self, amp):
        if isinstance(amp, (int, float)):  # Check if the input is a number
            self.amp = amp
        else:
            raise ValueError("amplitude must be a number")

    def set_wavnum(self, wavnum):
        if isinstance(wavnum, (int, float)):  # Check if the input is a number
            self.wavnum = wavnum
        else:
            raise ValueError("wave number must be a number")

    def set_phase(self, phase):
        if isinstance(phase, (int, float)):
            self.phase = phase
        else:
            raise ValueError("phase must be a number")

    def set_angfreq(self, angfreq):
        if isinstance(angfreq, (int, float)):  # Check if the input is a number
            self.angfreq = angfreq
        else:
            raise ValueError("angle frequency must be a number")

    def equation(self, x):
        p1 = self.wavnum * x
        p2 = self.angfreq * self.time
        p3 = p1 - p2 + self.phase
        y = self.amp * math.cos(p3)
        self.time += 0.1
        return (y)

    def wave_points(self):
        points = []
        points.clear()
        for each in range(240, 1199):
            y = Waves.equation(self, each)
            points.append((each, y))
        return points

    def wave_draw(self):
        points = Waves.wave_points(self)
        pygame.draw.lines(screen, red, False, points)


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
    output = TextBox(screen, x, y, width, height, fontSize=35)
    output.disable()
    return (output)


running = True
current_screen = ["menu"]
clicked = False

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
        header = pygame.draw.rect(screen, dgrey, rectangle(10, 1, 0, 0, False))
        # creates the bar at the top of the screen
        title_box = pygame.draw.rect(screen, grey, rectangle(2, 0.45, 4, 0.25, True))
        # creates the title box at the top of the screen
        back_button = pygame.draw.rect(screen, purple, rectangle(1, 0.4, 0.25, 0.25, False))
        # creates the back button
        if pos_check(back_button):
            back_button = pygame.draw.rect(screen, orange, rectangle(1, 0.4, 0.25, 0.25, False))
            # changes the colour of the back button when hovered
            if event.type == pygame.MOUSEBUTTONDOWN and len(current_screen) > 1:
                current_screen.pop()
                print(current_screen)
                sim_run = False

    if current_screen[-1] == "menu":  # defines the polygons on the menu screen-----------------------------------
        clicked = True
        # Charge Button
        chrg_button_points = hexagon(380, 350, 20)  # calculates each of the points for the hexagon
        chrg_button = poly_draw(purple, blue, chrg_button_points)  # draws the hexagon on screen with outline
        chrg_rect = poly_rect(chrg_button_points)  # creates the rect around the polygon for it to be interactable
        # Mass Button
        mass_button_points = hexagon(580, 670, 20)
        mass_button = poly_draw(purple, blue, mass_button_points)
        mass_rect = poly_rect(mass_button_points)
        # Wave Button
        wave_button_points = hexagon(780, 350, 20)
        wave_button = poly_draw(purple, blue, wave_button_points)
        wave_rect = poly_rect(wave_button_points)

        if chrg_rect.collidepoint(pygame.mouse.get_pos()):
            chrg_button = poly_draw(orange, blue, chrg_button_points)
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_screen.append("charge_sim")

        if mass_rect.collidepoint((pygame.mouse.get_pos())):
            mass_button = poly_draw(orange, blue, mass_button_points)
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_screen.append("mass_sim")

        if wave_rect.collidepoint((pygame.mouse.get_pos())):
            wave_button = poly_draw(orange, blue, wave_button_points)
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_screen.append("wave_sim")

    if current_screen[-1] == "charge_sim":  # ---------------------------------------------------------------
        sidebar = pygame.draw.rect(screen, red, rectangle(2, 9, 0, 1, False))
        # print(current_screen)
        backgrnd1 = pygame.draw.rect(screen, black, rectangle(10, 10, 2, 1, False))
        if clicked == True:
            slider1 = draw_slider(screen, 50, 458, 150, 20, -100, 100, 1)
            output1 = draw_output(screen, 175, 400, 50, 50)
            slider2 = draw_slider(screen, 50, 558, 150, 20, -100, 100, 1)
            output2 = draw_output(screen, 175, 500, 50, 50)
            slider3 = draw_slider(screen, 50, 658, 150, 20, 1, 100, 1)
            output3 = draw_output(screen, 175, 600, 50, 50)
            clicked = False
        slider1.listen(events)
        output1.setText(slider1.getValue())
        slider2.listen(events)
        output2.setText(slider2.getValue())
        slider3.listen(events)
        output3.setText(slider3.getValue())

        if backgrnd1.collidepoint(pygame.mouse.get_pos()):
            mousex, mousey = pygame.mouse.get_pos()
            # print(mousex,mousey)
            if event.type == pygame.MOUSEBUTTONDOWN:
                instance1 = Coulombs(slider1.getValue(), slider2.getValue(), slider3.getValue(), mousex, mousey)
                sim_run = True
        if sim_run == True:
            print("sim")
            instance1.update_position()
            instance1.draw(screen)
            instance1.set_q1(slider1.getValue())
            instance1.set_q2(slider2.getValue())
            instance1.set_m(slider3.getValue())

    if current_screen[-1] == "mass_sim":  # -------------------------------------------------------------------
        sidebar = pygame.draw.rect(screen, blue, rectangle(2, 9, 0, 1, False))
        print(current_screen)
        backgrnd1 = pygame.draw.rect(screen, black, rectangle(10, 10, 2, 1, False))
        if backgrnd1.collidepoint(pygame.mouse.get_pos()):
            mousex, mousey = pygame.mouse.get_pos()
            print(mousex, mousey)
        if clicked == True:
            slider1 = draw_slider(screen, 50, 458, 150, 20, -100, 100, 1)
            output1 = draw_output(screen, 175, 400, 50, 50)
            slider2 = draw_slider(screen, 50, 558, 150, 20, -100, 100, 1)
            output2 = draw_output(screen, 175, 500, 50, 50)
            slider3 = draw_slider(screen, 50, 658, 150, 20, -100, 100, 1)
            output3 = draw_output(screen, 175, 600, 50, 50)
            slider4 = draw_slider(screen, 50, 758, 150, 20, -100, 100, 1)
            output4 = draw_output(screen, 175, 700, 50, 50)
            wave = Waves(slider1.getValue(), slider2.getValue(), slider3.getValue(), slider4.getValue())
            clicked = False
        slider1.listen(events)
        output1.setText(slider1.getValue())
        slider2.listen(events)
        output2.setText(slider2.getValue())
        slider3.listen(events)
        output3.setText(slider3.getValue())
        slider4.listen(events)
        output4.setText(slider4.getValue())
        wave.wave_draw()
        wave.set_amp(slider1.getValue())
        wave.set_phase(slider2.getValue())
        wave.set_wavnum((slider3.getValue()))
        wave.set_angfreq(slider4.getValue())
        # instance2 = Coulombs()

    if current_screen[-1] == "wave_sim":
        sidebar = pygame.draw.rect(screen, green, rectangle(2, 9, 0, 1, False))
        print(current_screen)
        backgrnd1 = pygame.draw.rect(screen, black, rectangle(10, 10, 2, 1, False))
        if backgrnd1.collidepoint(pygame.mouse.get_pos()):
            mousex, mousey = pygame.mouse.get_pos()
            print(mousex, mousey)
        if clicked == True:
            slider1 = draw_slider(screen, 50, 458, 150, 20, -100, 100, 1)
            output1 = draw_output(screen, 175, 400, 50, 50)
            slider2 = draw_slider(screen, 50, 558, 150, 20, -100, 100, 1)
            output2 = draw_output(screen, 175, 500, 50, 50)
            slider3 = draw_slider(screen, 50, 658, 150, 20, -100, 100, 1)
            output3 = draw_output(screen, 175, 600, 50, 50)
            slider4 = draw_slider(screen, 50, 758, 150, 20, -100, 100, 1)
            output4 = draw_output(screen, 175, 700, 50, 50)
            wave = Waves(slider1.getValue(), slider2.getValue(), slider3.getValue(), slider4.getValue())
            clicked = False
        slider1.listen(events)
        output1.setText(slider1.getValue())
        slider2.listen(events)
        output2.setText(slider2.getValue())
        slider3.listen(events)
        output3.setText(slider3.getValue())
        slider4.listen(events)
        output4.setText(slider4.getValue())
        wave.wave_draw()

    if current_screen[-1] == "mass_sim" or current_screen[-1] == "charge_sim" or current_screen[-1] == "wave_sim":
        pygame_widgets.update(events)
        # instance1 = Waves()
