import pygame_widgets
import pygame
import time
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox
# Initialize Pygame
pygame.init()

# Window dimensions
global HEIGHT
global WIDTH
WIDTH, HEIGHT = 1200, 850

# Create the display surface
screen = pygame.display.set_mode((WIDTH, HEIGHT))

w_mid = WIDTH / 2
h_mid = HEIGHT / 2
screen_w_tenth = WIDTH / 10
screen_h_tenth = HEIGHT / 10

# Set the window title
pygame.display.set_caption("Colliding Circles")

# colours
if True:
    Lgrey = (200, 200, 200)
    grey = (100, 100, 100)
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 200, 0)
    red = (200, 0, 0)
    background_blue = (0, 5, 86)
    blue = (0, 117, 200)
    orange = (255, 127, 0)


# box maker
def box_maker(x, y, width, height, centre):
    w = width * screen_w_tenth
    h = height * screen_h_tenth
    x = x * screen_w_tenth
    y = y * screen_h_tenth
    if centre == True:
        x = w_mid - (w / 2)
    return (x, y, w, h)


# collsion detector (mouse to box)
def is_mouse_over_button(button_rect):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return button_rect.collidepoint(mouse_x, mouse_y)

def simulation_screen():
    # Sets up filter part on left hand side
    section1 = pygame.draw.rect(screen, grey, box_maker(section1_x, tosh, section1_w, 8, False))

    # Sets up display for simulation thumbnails
    section2 = pygame.draw.rect(screen, Lgrey, box_maker(section2_x, tosh, section2_w, 8, False))

    # Sets up movable divider on screen
    divider1 = pygame.draw.rect(screen, black, box_maker(section2_x, tosh, 0.1, 8, False))
    slider1 = Slider(screen, 200, 200, 200, 40, min=0, max=99, step=0.5, colour=blue, handlecolour=green, )
    slider2 = Slider(screen, 200, 400, 200, 40, min=0, max=99, step=0.5, colour=blue, handlecolour=green, )
    slider3 = Slider(screen, 200, 600, 200, 40, min=0, max=99, step=0.5, colour=blue, handlecolour=green, )
    slider4 = Slider(screen, 200, 800, 200, 40, min=0, max=99, step=0.5, colour=blue, handlecolour=green, )
    output = TextBox(screen, 475, 200, 50, 50, fontSize=30)
    pygame.display.update()
    output.setText(slider1.getValue())
    output.disable()



running = True
current_menu = ['main']
mode_selection_menu = False
general_simulations_mode = False
back_button = False
section1_x, section1_w = 0, 2
section2_x, section2_w = section1_w, 10 - section1_w
contback = True
contfor = True

while running:
    if contback == False:
        time.sleep(2)
        contback = True

    if contfor == False:
        time.sleep(2)
        contfor = True
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = event.pos
    pygame.display.update()
    screen.fill(Lgrey)

    top_of_screen_height = 1.5
    tosh = top_of_screen_height



    if current_menu[-1] != 'main': # menu at the top of each page
        # contains back button, name of prgram and profile button
        top_of_screen = pygame.draw.rect(screen, grey, box_maker(0, 0, 10, tosh, False))
        top_of_screen_outline = pygame.draw.rect(screen, black, box_maker(0, tosh - 0.1, 10, 0.11, False))
        name_box = pygame.draw.rect(screen, blue, box_maker(0, 0.1, 4, 1.2, True))
        if back_button == True:
            back_box = pygame.draw.rect(screen, red, box_maker(0.1, 0.1, 1, 0.5, False))
            if is_mouse_over_button(back_box):
                pygame.draw.rect(screen, green, back_box)  # Highlight when hovered
                if event.type == pygame.MOUSEBUTTONDOWN and contback == True:
                    current_menu.pop()
                    contback = False

    if current_menu[-1] == 'main':

        name_box = pygame.draw.rect(screen, blue, box_maker(0, 1.7, 4, 2, True))
        login_box = pygame.draw.rect(screen, blue, (box_maker(0, 4.5, 3, 1, True)))
        # Check if the mouse is over the buttons and change their appearance
        if is_mouse_over_button(login_box):
            pygame.draw.rect(screen, green, login_box)  # Highlight when hovered
            if event.type == pygame.MOUSEBUTTONDOWN and contfor == True:
                current_menu.append('mode_selection_menu')
                contfor = False
                back_button = True

    if current_menu[-1] == 'mode_selection_menu':

        box1 = pygame.draw.rect(screen, blue, box_maker(1.7, tosh + 1, 2.7, 6, False))
        #box2 = pygame.draw.rect(screen, blue, box_maker(3.65, tosh + 1, 2.7, 6, False))
        box3 = pygame.draw.rect(screen, blue, box_maker(5.3, tosh + 1, 2.7, 6, False))

        if is_mouse_over_button(box1):
            pygame.draw.rect(screen, green, box1)  # Highlight when hovered
            if event.type == pygame.MOUSEBUTTONDOWN and contfor == True:
                current_menu.append('charge_simulation_mode')
                contfor = False


        if is_mouse_over_button(box3):
            pygame.draw.rect(screen, green, box3)  # Highlight when hovered
            if event.type == pygame.MOUSEBUTTONDOWN and contfor == True:
                current_menu.append('mass_simulation_mode')
                contfor = False

    if current_menu[-1] == 'charge_simulations_mode':
        go = simulation_screen()


# similar to the main algorithm just uses mass instead of charge.
    if current_menu[-1] == 'mass_simulation_mode':
      go = simulation_screen()

    pygame_widgets.update(events)
    pygame.display.update()
