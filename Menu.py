import pygame

swidth, sheight = 1200, 1000

x_mid = swidth / 2
y_mid = sheight / 2
pygame.display.set_caption("Physics simulations")

screen = pygame.display.set_mode((swidth,sheight))

dgrey = (47, 54, 52)
grey = (100, 100, 100)
black = (17, 18, 18)
white = (255, 255, 255)
green = (0, 200, 0)
red = (200, 0, 0)
background_blue = (0, 5, 86)
blue = (0, 117, 200)
orange = (255, 127, 0)
purple = (76,0,153)

def hexagon(x,y,scale,colour1,colour2): # creates a hexagonal button
    multi1 = scale*10
    multi2 = scale*5
    multi3 = scale*11
    p1 = (x+multi1,y+multi2)
    p2 = (x+multi1,y-multi2)
    p3 = (x,y-multi3)
    p4 = (x-multi1,y-multi2)
    p5 = (x-multi1,y+multi2)
    p6 = (x,y+multi3)
    pygame.draw.polygon(screen,colour1,[p1,p2,p3,p4,p5,p6],0)
    pygame.draw.polygon(screen, colour2, [p1, p2, p3, p4, p5, p6], 4)

def rectangle(width,height,x,y,centre):
    w = width * swidth/10
    h = height * sheight/10
    x = x * swidth/10
    y = y * sheight/10
    if centre == True:
        x = x_mid - (w / 2)
    return (x, y, w, h)

def pos_check(button_poly):
    mousex,mousey = pygame.mouse.get_pos()
    return button_poly.collidepoint(mousex, mousey)


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
        header = pygame.draw.rect(screen,dgrey,rectangle(10,1,0,0,False))
        title_box = pygame.draw.rect(screen,grey,rectangle(2,0.45,4,0.25,True))

    if current_screen[-1] == "menu":
        chrg_button = hexagon(380,350,20,purple,blue)
        mass_button = hexagon(580,670,20,purple,blue)
        wave_button = hexagon(780,350,20,purple,blue)

        if pos_check(chrg_button):
            chrg_button = hexagon(380,350,20,orange,blue)



