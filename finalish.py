#https://lampz.tugraz.at/~hadley/physikm/script/waves/wave.en.php

import pygame
import math
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

k = 8.99 * (10 ^ 9)
pygame.font.init()


class Coulombs():
    def __init__(self, s, u, v, a, t, f, q1, q2, r, ):
        self.s = 0
        self.u = 0
        self.v = 0
        self.a = 0
        self.t = 0
        # Coulombs
        self.f = f
        self.q1 = q1
        self.q2 = q2

        self.r = r
        # Newton's second law
        self.mass = 1.6*(10**(-16))
        # also uses F and a, but they are already defined
        self.p1x = 704
        self.p1y = 504
        self.p2x = 0
        self.p2y = 0
        self.grad = 1

    def coulombs(self):
        qt = self.q1 * self.q2
        denom = k * (self.r ** 2)
        self.f = qt / denom

    def nsl(self):  # newtons second law
        self.a = self.f / self.mass

    def suvat(self):
        step1 = self.u * self.t
        step2 = self.a * (self.t ** 2)
        step3 = step2 * 0.5
        self.s = self.s + step1 + step3

    def set_p2x(self,mousex):
        self.p2x = mousex

    def set_p2y(self, mousey):
        self.p2y = mousey

    def line(self):
        grady = self.p2y - self.p1y
        gradx = self.p2x - self.p1x
        self.grad = grady / gradx
    
    


class Waves():
    def __init__(self, amp, wavnum, phase, angfreq, x):
        self.amp = amp
        self.wavnum = wavnum
        self.phase = phase
        self.angfreq = angfreq
        self.time = 0
        self.run = False
        self.p4 = 0
        self.x = x

    def timer(self):
        while self.run == True:
            self.time += 0.1

    def equation(self):
        p1 = self.wavnum * self.x
        p2 = self.angfreq * self.time
        p3 = p1 - p2 + self.phase
        self.p4 = self.amp * math.cos(p3)


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
    multi1 = scale * 10
    multi2 = scale * 5
    multi3 = scale * 11
    p1 = (x + multi1, y + multi2)
    p2 = (x + multi1, y - multi2)
    p3 = (x, y - multi3)
    p4 = (x - multi1, y - multi2)
    p5 = (x - multi1, y + multi2)
    p6 = (x, y + multi3)
    points = [p1, p2, p3, p4, p5, p6]
    return points


def poly_draw(colour1, colour2, points, ):
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


slider1 = Slider(screen, 50, 458, 150, 20, min=-100, max=100, step=1)
output1 = TextBox(screen, 175, 400, 50, 50, fontSize=35)
slider2 = Slider(screen, 50, 558, 150, 20, min=-100, max=100, step=1)
output2 = TextBox(screen, 175, 500, 50, 50, fontSize=35)
slider3 = Slider(screen, 50, 658, 150, 20, min=-100, max=100, step=1)
output3 = TextBox(screen, 175, 600, 50, 50, fontSize=35)
output1.disable
output2.disable
output3.disable

        


running = True
current_screen = ["menu"]


while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = event.pos
          
    pygame.display.update()
    screen.fill(black)
    if current_screen[-1] != "login":           # draws the bar at the top of the screen
        header = pygame.draw.rect(screen, dgrey,
                                  rectangle(10, 1, 0, 0, False))  #creates the bar at the top of the screen
        title_box = pygame.draw.rect(screen, grey, rectangle(2, 0.45, 4, 0.25,
                                                             True))  # creates the title box at the top of the screen
        back_button = pygame.draw.rect(screen, purple, rectangle(1, 0.4, 0.25, 0.25, False))  # creates the back button
        if pos_check(back_button):
            back_button = pygame.draw.rect(screen, orange, rectangle(1, 0.4, 0.25, 0.25,
                                                                     False))  # changes the colour of the back button when hovered
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_screen[-1] = "menu"
                ran = False

    if current_screen[-1] == "menu":  # defines the polygons on the menu screen
        # Charge Button
        chrg_button_points = hexagon(380, 350, 20)  #calculates each of the points for the hexagon
        chrg_button = poly_draw(purple, blue, chrg_button_points)  #draws the hexagon on screen with outline
        chrg_rect = poly_rect(chrg_button_points)  #creates the rect around the polygon for it to be interactable
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
                current_screen[-1] = "charge_sim"

        if mass_rect.collidepoint((pygame.mouse.get_pos())):
            mass_button = poly_draw(orange, blue, mass_button_points)
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_screen[-1] = "mass_sim"

        if wave_rect.collidepoint((pygame.mouse.get_pos())):
            wave_button = poly_draw(orange, blue, wave_button_points)
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_screen[-1] = "wave_sim"

    if current_screen[-1] == "charge_sim":
        sidebar = pygame.draw.rect(screen, red, rectangle(2, 9, 0, 1, False))
        print(current_screen)
        backgrnd1 = pygame.draw.rect(screen, black, rectangle(10, 10, 2, 1, False))

        if backgrnd1.collidepoint(pygame.mouse.get_pos()):
            mousex , mousey = pygame.mouse.get_pos()
            print(mousex,mousey)
        output1.setText(slider1.getValue())
        slider1.listen(events)
        output2.setText(slider2.getValue())
        slider2.listen(events)
        output3.setText(slider3.getValue())
        slider3.listen(events)
        instance2 = Coulombs()

    if current_screen[-1] == "mass_sim":
        sidebar = pygame.draw.rect(screen, blue, rectangle(2, 9, 0, 1, False))
        print(current_screen)
        backgrnd1 = pygame.draw.rect(screen, black, rectangle(10, 10, 2, 1, False))
        if backgrnd1.collidepoint(pygame.mouse.get_pos()):
            mousex, mousey = pygame.mouse.get_pos()
            print(mousex, mousey)

    
        

        #instance2 = Coulombs()

    if current_screen[-1] == "wave_sim":
        sidebar = pygame.draw.rect(screen, green, rectangle(2, 9, 0, 1, False))
        print(current_screen)
        backgrnd1 = pygame.draw.rect(screen, black, rectangle(10, 10, 2, 1, False))
        if backgrnd1.collidepoint(pygame.mouse.get_pos()):
            mousex, mousey = pygame.mouse.get_pos()
            print(mousex, mousey)

    if current_screen[-1] == "mass_sim" or current_screen[-1] == "charge_sim":
        pygame_widgets.update(events)  
        #instance1 = Waves()
