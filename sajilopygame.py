import math
import pygame
import random
from pygame import mixer

class sajilopygame:
    def __init__(self,wwidth=800,wheight=600):
        self.wwidth = wwidth
        self.wheight = wheight

        # initializing pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.wwidth,self.wheight))

        # Movement states for keys
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.trigger_pressed = False

        # Mappings
        self.is_lr_mapped_to_player = False
        self.is_ud_mapped_to_player = False
        self.is_lr_mapped_to_enemy = False
        self.is_ud_mapped_to_enemy = False
        self.is_lr_mapped_to_object = False
        self.is_ud_mapped_to_object = False

        # edge detection
        self.last_detected_edge_player = None
        self.last_detected_edge_enemy = None
        self.last_detected_edge_object = None

        # for assigning triggers
        self.selected_trigger_type = "object"
        self.selected_trigger_dir = "b2t"
        self.selected_trigger_speed = 1
        self.triggered_state = False
        self.end_trigger = False

        # collisions
        self.collision_state = False
        self.collision_type = "enemy"
        self.collision_effect = "disappear"
        self.collision_count = 0

        # limits
        self.random_ximit = (0,0)
        self.random_yimit = (0,0)

        # sounds
        self.collision_sound_path = None
        self.collision_sound_volume = 0.5
        self.collision_sound_activated = False
        self.random_sound_path = None
        self.random_sound_volume = 0.5
        self.random_sound_activated = False
        self.trigger_sound_path = None
        self.trigger_sound_volume = 0.5
        self.trigger_sound_activated = False

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
                if event.key == pygame.K_SPACE:
                    self.trigger_pressed = True

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
                if event.key == pygame.K_SPACE:
                    self.trigger_pressed = False

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

        # incase there is a trigger press
        if self.trigger_pressed:
            self.triggered_state = True
            self.trigger_pressed = False

        if self.triggered_state:
            self.trigger()

        # collisions
        if self.collision_state:
            self.collision_count += 1
            print(self.collision_count)
            self.collision_state = False    # resetting the value
            if self.collision_effect == "disappear":
                if self.collision_type == "enemy":
                    x, y = self.enemyx, self.enemyy
                if self.collision_type == "object":
                    x, y = self.objectx, self.objecty
                if self.collision_type == "player":
                    x, y = self.playerx, self.playery
                self.update_position(type=self.collision_type,xpos=x-self.wwidth,ypos=y-self.wheight)
            if self.collision_effect == "random":
                self.move_to_random(type=self.collision_type)


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

    # assign Left, Right keystrokes
    def assign_lr_keys(self,type="player",intensity=(1,1)):
        if type == "player":
            self.is_lr_mapped_to_player = True
            self.player_l_intensity, self.player_r_intensity = intensity
        if type == "enemy":
            self.is_lr_mapped_to_enemy = True
            self.enemy_l_intensity, self.enemy_r_intensity = intensity
        if type == "object":
            self.is_lr_mapped_to_object = True
            self.object_l_intensity, self.object_r_intensity = intensity

    # assign Up, Down keystrokes
    def assign_ud_keys(self,type="player",intensity=(1,1)):
        if type == "player":
            self.is_ud_mapped_to_player = True
            self.player_u_intensity, self.player_d_intensity = intensity
        if type == "enemy":
            self.is_ud_mapped_to_enemy = True
            self.enemy_u_intensity, self.enemy_d_intensity = intensity
        if type == "object":
            self.is_ud_mapped_to_object = True
            self.object_u_intensity, self.object_d_intensity = intensity

    # getting the positions
    def find_position(self,type="player"):
        if type == "player":
            return self.playerx, self.playery
        if type == "enemy":
            return self.enemyx, self.enemyy
        if type == "object":
            return self.objectx, self.objecty

    # update position
    def update_position(self,type="player",xpos=0,ypos=0):
        if type == "player":
            self.playerx = xpos
            self.playery = ypos
        if type == "enemy":
            self.enemyx = xpos
            self.enemyy = ypos
        if type == "object":
            self.objectx = xpos
            self.objecty = ypos

    # getting the size
    def find_size(self,type="player"):
        if type == "player":
            return self.player_width, self.player_height
        if type == "enemy":
            return self.enemy_width, self.enemy_height
        if type == "object":
            return self.object_width, self.object_height

    # bounding to the window
    def bound_to_window(self,type="player"):
        if type == "player":
            if self.playerx < 0:
                self.playerx = 0
            elif self.playerx > self.wwidth - self.player_width:
                self.playerx = self.wwidth - self.player_width
            if self.playery < 0:
                self.playery = 0
            elif self.playery > self.wheight - self.player_height:
                self.playery = self.wheight - self.player_height
        if type == "enemy":
            if self.enemyx < 0:
                self.enemyx = 0
            elif self.enemyx > self.wwidth - self.enemy_width:
                self.enemyx = self.wwidth - self.enemy_width
            if self.enemyy < 0:
                self.enemyy = 0
            elif self.enemyy > self.wheight - self.enemy_height:
                self.enemyy = self.wheight - self.enemy_height
        if type == "object":
            if self.objectx < 0:
                self.objectx = 0
            elif self.objectx > self.wwidth - self.object_width:
                self.objectx = self.wwidth - self.object_width
            if self.objecty < 0:
                self.objecty = 0
            elif self.objecty > self.wheight - self.object_height:
                self.objecty = self.wheight - self.object_height

    # move from left to right
    def move_left_to_right(self,type="enemy",speed=1):
        if type == "enemy":
            self.enemyx = self.enemyx + speed
        if type == "object":
            self.objectx = self.objectx + speed
        if type == "player":
            self.playerx = self.playerx + speed

    # move from right to left
    def move_right_to_left(self,type="enemy",speed=1):
        if type == "enemy":
            self.enemyx = self.enemyx - speed
        if type == "object":
            self.objectx = self.objectx - speed
        if type == "player":
            self.playerx = self.playerx - speed

    # move from up to down
    def move_top_to_bottom(self,type="enemy",speed=1):
        if type == "enemy":
            self.enemyy = self.enemyy + speed
        if type == "object":
            self.objecty = self.objecty + speed
        if type == "player":
            self.playery = self.playery + speed

    # move from down to up
    def move_bottom_to_top(self,type="enemy",speed=1):
        if type == "enemy":
            self.enemyy = self.enemyy - speed
        if type == "object":
            self.objecty = self.objecty - speed
        if type == "player":
            self.playery = self.playery - speed

    # edge detection
    def detect_edge(self,type="enemy"):
        if type == "player":
            if self.playerx == 0:
                self.last_detected_edge_player = "left"
            if self.playerx == self.wwidth-self.player_width:
                self.last_detected_edge_player = "right"
            if self.playery == 0:
                self.last_detected_edge_player = "top"
            if self.playery == self.wheight-self.enemy_height:
                self.last_detected_edge_player = "bottom"
        if type == "enemy":
            if self.enemyx == 0:
                self.last_detected_edge_enemy = "left"
            if self.enemyx == self.wwidth-self.enemy_width:
                self.last_detected_edge_enemy = "right"
            if self.enemyy == 0:
                self.last_detected_edge_enemy = "top"
            if self.enemyy == self.wheight-self.enemy_height:
                self.last_detected_edge_enemy = "bottom"
        if type == "object":
            if self.objectx == 0:
                self.last_detected_edge_object = "left"
            if self.objectx == self.wwidth-self.object_width:
                self.last_detected_edge_object = "right"
            if self.objecty == 0:
                self.last_detected_edge_object = "top"
            if self.objecty == self.wheight-self.object_height:
                self.last_detected_edge_object = "bottom"

        if type == "player":
            return self.last_detected_edge_player
        elif type == "object":
            return self.last_detected_edge_object
        elif type == "enemy":
            return self.last_detected_edge_enemy

    # bouncing left and right
    def bounce_left_right(self,type="enemy",speed=1):
        edge = self.detect_edge(type=type)

        if edge == "left":
            self.move_left_to_right(type=type, speed=speed)
        elif edge == "right":
            self.move_right_to_left(type=type, speed=speed)
        else:
            self.move_left_to_right(type=type, speed=speed)

    # bouncing top and bottom
    def bounce_top_bottom(self,type="enemy",speed=1):
        edge = self.detect_edge(type=type)

        if edge == "top":
            self.move_top_to_bottom(type=type, speed=speed)
        elif edge == "bottom":
            self.move_bottom_to_top(type=type, speed=speed)
        else:
            self.move_top_to_bottom(type=type, speed=speed)

    # releasing
    def assign_trigger(self,type="object",start_pos=(370,240),dir="b2t",speed=1):
        x,y = start_pos
        if self.end_trigger == False:
            self.update_position(type=type,xpos=x,ypos=y)
            self.end_trigger = True
        self.selected_trigger_type = type
        self.selected_trigger_dir = dir
        self.selected_trigger_speed = speed

    # triggering
    def trigger(self):
        if self.selected_trigger_type == "object":
            if self.selected_trigger_dir == "b2t":
                self.move_bottom_to_top(type=self.selected_trigger_type, speed=self.selected_trigger_speed)
                x, y = self.find_position(type="object")
                if y <= 0-self.object_height:
                    self.triggered_state = False
                    self.end_trigger = False
            if self.selected_trigger_dir == "t2b":
                self.move_top_to_bottom(type=self.selected_trigger_type, speed=self.selected_trigger_speed)
                x, y = self.find_position(type="object")
                if y >= self.wheight + self.object_height:
                    self.triggered_state = False
                    self.end_trigger = False
            if self.selected_trigger_dir == "r2l":
                self.move_right_to_left(type=self.selected_trigger_type, speed=self.selected_trigger_speed)
                x, y = self.find_position(type="object")
                if x <= 0-self.object_width:
                    self.triggered_state = False
                    self.end_trigger = False
            if self.selected_trigger_dir == "l2r":
                self.move_left_to_right(type=self.selected_trigger_type, speed=self.selected_trigger_speed)
                x, y = self.find_position(type="object")
                if x >= self.wwidth + self.object_width:
                    self.triggered_state = False
                    self.end_trigger = False
        # for player
        if self.selected_trigger_type == "player":
            if self.selected_trigger_dir == "b2t":
                self.move_bottom_to_top(type=self.selected_trigger_type, speed=self.selected_trigger_speed)
                x, y = self.find_position(type="player")
                if y <= 0-self.player_height:
                    self.triggered_state = False
                    self.end_trigger = False
            if self.selected_trigger_dir == "t2b":
                self.move_top_to_bottom(type=self.selected_trigger_type, speed=self.selected_trigger_speed)
                x, y = self.find_position(type="player")
                if y >= self.wheight + self.player_height:
                    self.triggered_state = False
                    self.end_trigger = False
            if self.selected_trigger_dir == "r2l":
                self.move_right_to_left(type=self.selected_trigger_type, speed=self.selected_trigger_speed)
                x, y = self.find_position(type="player")
                if x <= 0-self.player_width:
                    self.triggered_state = False
                    self.end_trigger = False
            if self.selected_trigger_dir == "l2r":
                self.move_left_to_right(type=self.selected_trigger_type, speed=self.selected_trigger_speed)
                x, y = self.find_position(type="player")
                if x >= self.wwidth + self.player_width:
                    self.triggered_state = False
                    self.end_trigger = False
        # for enemy
        if self.selected_trigger_type == "enemy":
            if self.selected_trigger_dir == "b2t":
                self.move_bottom_to_top(type=self.selected_trigger_type, speed=self.selected_trigger_speed)
                x, y = self.find_position(type="enemy")
                if y <= 0-self.enemy_height:
                    self.triggered_state = False
                    self.end_trigger = False
            if self.selected_trigger_dir == "t2b":
                self.move_top_to_bottom(type=self.selected_trigger_type, speed=self.selected_trigger_speed)
                x, y = self.find_position(type="enemy")
                if y >= self.wheight + self.enemy_height:
                    self.triggered_state = False
                    self.end_trigger = False
            if self.selected_trigger_dir == "r2l":
                self.move_right_to_left(type=self.selected_trigger_type, speed=self.selected_trigger_speed)
                x, y = self.find_position(type="enemy")
                if x <= 0-self.enemy_width:
                    self.triggered_state = False
                    self.end_trigger = False
            if self.selected_trigger_dir == "l2r":
                self.move_left_to_right(type=self.selected_trigger_type, speed=self.selected_trigger_speed)
                x, y = self.find_position(type="enemy")
                if x >= self.wwidth + self.enemy_width:
                    self.triggered_state = False
                    self.end_trigger = False
        # checking for sound in trigger and activating it
        if self.trigger_sound_activated:
            self.trigger_sound = pygame.mixer.Sound(self.trigger_sound_path)
            self.trigger_sound.set_volume(self.trigger_sound_volume)
            self.trigger_sound.play()

    # assigning collision effects
    def assign_collision_effect(self,type="enemy",effect="disappear"):
        self.collision_type = type
        self.collision_effect = effect

    # assign collision limits
    def limit_randomness(self,type="enemy",xlimit=(0,0),ylimit=(0,0)):
        self.random_ximit = xlimit
        self.random_ylimit = ylimit
        lower_xlimit, upper_xlimit = self.random_ximit
        upper_ylimit, lower_ylimit = self.random_ylimit
        xpos, ypos = self.find_position(type=type)
        if lower_xlimit <= xpos <= upper_xlimit or lower_ylimit <= ypos <= upper_ylimit:
            self.move_to_random(type=type)

    # collision detection
    def detect_collision(self,collision_by="object",collision_with="enemy"):
        collision_by_x, collision_by_y = self.find_position(type=collision_by)

        collision_with_x, collision_with_y = self.find_position(type=collision_with)

        distance = math.sqrt((math.pow(collision_with_x-collision_by_x,2)) + (math.pow(collision_with_y-collision_by_y,2)))
        if distance <= 50:  # this i am yet to determine, but i am just giving a threshold at this point
            self.collision_state = True
            # checking for collision sound and activating it
            if self.collision_sound_activated:
                self.collision_sound = pygame.mixer.Sound(self.collision_sound_path)
                self.collision_sound.set_volume(self.collision_sound_volume)
                self.collision_sound.play()
        else:
            self.collision_state = False

    # function to move to random place
    def move_to_random(self, type="enemy"):
        if type == "player":
            self.playerx = random.randint(0, self.wwidth - self.player_width)
            self.playery = random.randint(0, self.wheight - self.player_height)
        if type == "enemy":
            self.enemyx = random.randint(0, self.wwidth - self.enemy_width)
            self.enemyy = random.randint(0, self.wheight - self.enemy_height)
        if type == "object":
            self.objectx = random.randint(0, self.wwidth - self.object_width)
            self.objecty = random.randint(0, self.wheight - self.object_height)
        # checking for sound in randomness and activating it
        if self.random_sound_activated:
            self.random_sound = pygame.mixer.Sound(self.random_sound_path)
            self.random_sound.set_volume(self.random_sound_volume)
            self.random_sound.play()

    # display score
    def display_score(self,score=0):
        score = self.collision_count
        score_font = pygame.font.SysFont("comicsansms", 30)
        score_text = score_font.render("Score : " + str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.center = (self.wwidth/2-300, 50)
        self.screen.blit(score_text, score_rect)

    # get score
    def get_score(self):
        return self.collision_count

    # loading sound
    def load_sound(self,sound_path=None,type="background",volume=0.5):
        if type == "background":
            self.background_sound = pygame.mixer.Sound(sound_path)
            self.background_sound.set_volume(volume)
            self.background_sound.play(-1)
        if type == "collision":
            self.collision_sound_path = pygame.mixer.Sound(sound_path)
            self.collision_sound_volume = volume
            self.collision_sound_activated = True
        if type == "random":
            self.random_sound_path = pygame.mixer.Sound(sound_path)
            self.random_sound_volume = volume
            self.random_sound_activated = True
        if type == "trigger":
            self.trigger_sound_path = pygame.mixer.Sound(sound_path)
            self.trigger_sound_volume = volume
            self.trigger_sound_activated = True