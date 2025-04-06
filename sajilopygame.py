import pygame

class sajilopygame:
    def __init__(self,swidth=800,sheight=600):
        self.swidth = swidth
        self.sheight = sheight

        # initializing pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.swidth,self.sheight))

        # Movement states for keys
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        # Mappings
        self.is_lr_mapped_to_player = False
        self.is_ud_mapped_to_player = False
        self.is_lr_mapped_to_enemy = False
        self.is_ud_mapped_to_enemy = False
        self.is_lr_mapped_to_object = False
        self.is_ud_mapped_to_object = False

    # function to update the display window
    # also is responsible for quitting the program
    def refresh_window(self):
        # updating the window
        pygame.display.update()

        # Checking for window events
        for event in pygame.event.get():
            # If close button is pressed
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            # upon key presses
            if event.type == pygame.KEYDOWN:
                # If Esc button is pressed
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                # Movement key pressed
                if event.key == pygame.K_LEFT:
                    self.left_pressed = True
                if event.key == pygame.K_RIGHT:
                    self.right_pressed = True
                if event.key == pygame.K_UP:
                    self.up_pressed = True
                if event.key == pygame.K_DOWN:
                    self.down_pressed = True

            # Upon key release
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_pressed = False
                if event.key == pygame.K_RIGHT:
                    self.right_pressed = False
                if event.key == pygame.K_UP:
                    self.up_pressed = False
                if event.key == pygame.K_DOWN:
                    self.down_pressed = False

        # Update player position based on the key press state
        if self.is_lr_mapped_to_player:
            if self.left_pressed:
                self.playerx -= self.player_l_intensity
            if self.right_pressed:
                self.playerx += self.player_r_intensity
        if self.is_ud_mapped_to_player:
            if self.up_pressed:
                self.playery -= self.player_u_intensity
            if self.down_pressed:
                self.playery += self.player_d_intensity

        # Update enemy position based on the key press state
        if self.is_lr_mapped_to_enemy:
            if self.left_pressed:
                self.enemyx -= self.enemy_l_intensity
            if self.right_pressed:
                self.enemyx += self.enemy_r_intensity
        if self.is_ud_mapped_to_enemy:
            if self.up_pressed:
                self.enemyy -= self.enemy_u_intensity
            if self.down_pressed:
                self.enemyy += self.enemy_d_intensity

        # Update object position based on the key press state
        if self.is_lr_mapped_to_object:
            if self.left_pressed:
                self.objectx -= self.object_l_intensity
            if self.right_pressed:
                self.objectx += self.object_r_intensity
        if self.is_ud_mapped_to_object:
            if self.up_pressed:
                self.objecty -= self.object_u_intensity
            if self.down_pressed:
                self.objecty += self.object_d_intensity


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
        self.bg_width, self.bg_height = self.background.get_size()
        self.screen.blit(self.background,(0,0))

    # creating a player
    def create_player(self,image_path,org=(370,480)):
        self.playerx, self.playery = org
        self.player_img = pygame.image.load(image_path)
        self.player_width, self.player_height = self.player_img.get_size()

    # loading a player
    def load_player(self):
        self.screen.blit(self.player_img,(self.playerx,self.playery))

    # creating an enemy
    def create_enemy(self,image_path,org=(370,40)):
        self.enemyx, self.enemyy = org
        self.enemy_img = pygame.image.load(image_path)
        self.enemy_width, self.enemy_height = self.enemy_img.get_size()

    # loading an enemy
    def load_enemy(self):
        self.screen.blit(self.enemy_img,(self.enemyx,self.enemyy))

    # creating an object
    def create_object(self,image_path,org=(370,240)):
        self.objectx, self.objecty = org
        self.object_img = pygame.image.load(image_path)
        self.object_width, self.object_height = self.object_img.get_size()

    # loading an object
    def load_object(self):
        self.screen.blit(self.object_img,(self.objectx,self.objecty))

    # mapping Left, Right keystrokes to player
    def map_lr_keys_to_player(self,intensity=(1,1)):
        self.is_lr_mapped_to_player = True
        self.player_l_intensity, self.player_r_intensity = intensity

    # mapping Up, Down keystrokes to player
    def map_ud_keys_to_player(self,intensity=(1,1)):
        self.is_ud_mapped_to_player = True
        self.player_u_intensity, self.player_d_intensity = intensity

    # mapping Left, Right keystrokes to enemy
    def map_lr_keys_to_enemy(self,intensity=(1,1)):
        self.is_lr_mapped_to_enemy = True
        self.enemy_l_intensity, self.enemy_r_intensity = intensity

    # mapping Up, Down keystrokes to enemy
    def map_ud_keys_to_enemy(self,intensity=(1,1)):
        self.is_ud_mapped_to_enemy = True
        self.enemy_u_intensity, self.enemy_d_intensity = intensity

    # mapping Left, Right keystrokes to object
    def map_lr_keys_to_object(self,intensity=(1,1)):
        self.is_lr_mapped_to_object = True
        self.object_l_intensity, self.object_r_intensity = intensity

    # mapping Up, Down keystrokes to object
    def map_ud_keys_to_object(self,intensity=(1,1)):
        self.is_ud_mapped_to_object = True
        self.object_u_intensity, self.object_d_intensity = intensity