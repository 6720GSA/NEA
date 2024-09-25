import pygame



class Button(pygame.sprite.Sprite):
    def __init__(self, color, color_hover, rect, callback, text='', outline=None):
        super().__init__()
        self.text = text
        # a temporary Rect to store the size of the button
        tmp_rect = pygame.Rect(0, 0, *rect.size)

        # create two Surfaces here, one the normal state, and one for the hovering state
        # we create the Surfaces here once, so we can simple built them and dont have
        # to render the text and outline again every frame
        self.org = self._create_image(color, outline, text, tmp_rect)
        self.hov = self._create_image(color_hover, outline, text, tmp_rect)

        # in Sprites, the image attribute holds the Surface to be displayed...
        self.image = self.org
        # ...and the rect holds the Rect that defines it position
        self.rect = rect
        self.callback = callback

    def _create_image(self, color, outline, text, rect):
        img = pygame.Surface(rect.size)
        if outline:
            img.fill(outline)
            img.fill(color, rect.inflate(-4, -3))
        else:
            img.fill(color)

        # render the text once here instead of every frame
        if text != '':
            text_surf = font.render(text, 1, pygame.Color('black'))
            # again, see how easy it is to center stuff using Rect's
            # attributes like 'center'
            text_rect = text_surf.get_rect(center=rect.center)
            img.blit(text_surf, text_rect)
        return img

    def update(self, events):
        pos = pygame.mouse.get_pos()
        hit = self.rect.collidepoint(pos)

        self.image = self.hov if hit else self.org
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and hit:
                self.callback(self)

class Menu1:
    def __init__(self,):
        
        
    def first(self):
        sprites.add(Button(pygame.Color('green'),  # Button colour
                           pygame.Color('red'),  # hover colour
                           pygame.Rect(20, 100, 200, 200),  # size and location
                           lambda b: print(f"Button '{b.text}' was clicked"),  # Output
                           'Hover',  # Button text
                           pygame.Color('black'), ))  # Border Colour

        sprites.add(Button(pygame.Color('yellow'),
                           pygame.Color('red'),
                           pygame.Rect(300, 100, 200, 200),
                           lambda b: print(f"Click  me again!"),
                           'Another'))


pygame.init()
clock = pygame.time.Clock()
stack = [0]
font = pygame.font.Font(None, 24)

#Defining colours
BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# CREATING WINDOW
screen_size = (800, 800)
screen = pygame.display.set_mode(screen_size)

# TITLE OF WINDOW
pygame.display.set_caption("NEA Physics Simulations")
run = True
count = True
sprites = pygame.sprite.Group()


while run == True:

    if stack[0] == 0:
        if count == True:
            Menu1.first()
        
    clock.tick(60)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
    screen.fill(GRAY)
    sprites.update(events)
    sprites.draw(screen)
    pygame.display.update()


    pygame.display.update()
