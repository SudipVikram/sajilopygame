import pygame

class sajilopygame:
    def __init__(self,swidth=800,sheight=600):
        self.swidth = swidth
        self.sheight = sheight

        # initializing pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.swidth,self.sheight))

    # function to update the display window
    # also is responsible for quitting the program
    def refresh_window(self):
        # updating the window
        pygame.display.update()

        # checking for a close window event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    # loading the window title
    def window_title(self,title):
        pygame.display.set_caption(title)

    # loading the favicon
    def favicon(self,image_path):
        self.icon = pygame.image.load(image_path)
        pygame.display.set_icon(self.icon)

    # loading background color
    def background_color(self,color):
        self.screen.fill(color)

    # loading the background
    def background_image(self,image_path):
        self.background = pygame.image.load(image_path)
        self.screen.blit(self.background,(0,0))

    # loading a player
    def player(self,image_path,org=(370,480)):
        self.playerx, self.playery = org
        self.player = pygame.image.load(image_path)
        self.screen.blit(self.player,(self.playerx,self.playery))
