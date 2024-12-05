import pygame

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
    button_rect = pygame.Rect(min_x,min_y,max_x-min_x,max_y-min_y)
    return(button_rect)

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


#def poly_check(button):
#   points =

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
    if current_screen[-1] != "login":
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

    if current_screen[-1] == "menu":  # defines the polygons on the menu screen
        # Charge Button
        chrg_button_points = hexagon(380, 350, 10)  #calculates each of the points for the hexagon
        chrg_button = poly_draw(purple, blue, chrg_button_points)  #draws the hexagon on screen with outline
        chrg_rect = poly_rect(chrg_button_points)  #creates the rect around the polygon for it to be interactable
        # Mass Button
        mass_button_points = hexagon(580, 670, 10)
        mass_button = poly_draw(purple, blue, mass_button_points)
        mass_rect = poly_rect(mass_button_points)
        # Wave Button
        wave_button_points = hexagon(780, 350, 10)
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

    if current_screen[-1] == "mass_sim":
        sidebar = pygame.draw.rect(screen, blue, rectangle(2, 9, 0, 1, False))
        print(current_screen)

    if current_screen[-1] == "wave_sim":
        sidebar = pygame.draw.rect(screen, green, rectangle(2, 9, 0, 1, False))
        print(current_screen)
