"""
This is a library by Beyond Apogee, Nepal tailored
for the school-level students that we educate in our
robotics program.
@ developer: Beyond Apogee
@ author: Sudip Vikram Adhikari
@ version: 1.0
@ license: MIT
"""

import math
import os
import time

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

        # initializing time
        self.clock = pygame.time.Clock()
        self.fps = 60

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
        self.death_sound_path = None
        self.death_sound_volume = 0.5
        self.death_sound_activated = False
        self.victory_sound_path = None
        self.victory_sound_volume = 0.5
        self.victory_sound_activated = False

        # lives
        self.lives = 3
        self.game_over_state = False

        # transformations
        self.player_transformed = False

        # files
        self.HIGH_SCORE_FILE = "high_score.txt"

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

        # checking for game over
        if self.lives == 0:
            self.game_over()

        # setting the fps
        self.clock.tick(self.fps)


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
        self.player_image_path = image_path
        self.playerx, self.playery = org
        self.player_img = pygame.image.load(image_path).convert_alpha()
        self.player_width, self.player_height = self.player_img.get_size()
        self.player_rect = self.player_img.get_rect()

    # loading a player
    def load_player(self):
        if self.player_transformed:
            return      # transformation set in
        elif self.is_lr_mapped_to_player:
            # checking if there are other images for each keystroke
            pathname = os.path.dirname(self.player_image_path)
            image_name = self.player_image_path.split("/")[-1]
            image_name_wo_ext = image_name.split(".")[0]   # without extension
            image_ext = image_name.split(".")[-1]
            left_image_placeholder = pathname+'/'+image_name_wo_ext+"_left"+"."+image_ext
            up_left_image_placeholder = pathname+'/'+image_name_wo_ext+"_up_left"+"."+image_ext
            down_left_image_placeholder = pathname+'/'+image_name_wo_ext+"_down_left"+"."+image_ext
            right_image_placeholder = pathname+'/'+image_name_wo_ext+"_right"+"."+image_ext
            up_right_image_placeholder = pathname+'/'+image_name_wo_ext+"_up_right"+"."+image_ext
            down_right_image_placeholder = pathname+'/'+image_name_wo_ext+"_down_right"+"."+image_ext
            up_image_placeholder = pathname+'/'+image_name_wo_ext+"_up"+"."+image_ext
            down_image_placeholder = pathname+'/'+image_name_wo_ext+"_down"+"."+image_ext
            # checking for keystrokes
            if self.left_pressed and self.up_pressed:
                if os.path.exists(up_left_image_placeholder):
                    up_left_image = pygame.image.load(up_left_image_placeholder)
                    self.screen.blit(up_left_image,(self.playerx,self.playery))
            elif self.left_pressed and self.down_pressed:
                if os.path.exists(down_left_image_placeholder):
                    down_left_image = pygame.image.load(down_left_image_placeholder)
                    self.screen.blit(down_left_image,(self.playerx,self.playery))
            elif self.left_pressed and not self.up_pressed and not self.down_pressed:
                if os.path.exists(left_image_placeholder):
                    left_image = pygame.image.load(left_image_placeholder)
                    self.screen.blit(left_image,(self.playerx,self.playery))
                else:
                    self.screen.blit(self.player_img, (self.playerx, self.playery))
            elif self.right_pressed and self.up_pressed:
                if os.path.exists(up_right_image_placeholder):
                    up_right_image = pygame.image.load(up_right_image_placeholder)
                    self.screen.blit(up_right_image,(self.playerx,self.playery))
            elif self.right_pressed and self.down_pressed:
                if os.path.exists(down_right_image_placeholder):
                    down_right_image = pygame.image.load(down_right_image_placeholder)
                    self.screen.blit(down_right_image,(self.playerx,self.playery))
            elif self.right_pressed and not self.up_pressed and not self.down_pressed:
                if os.path.exists(right_image_placeholder):
                    right_image = pygame.image.load(right_image_placeholder)
                    self.screen.blit(right_image,(self.playerx,self.playery))
                else:
                    self.screen.blit(self.player_img, (self.playerx, self.playery))
            elif self.up_pressed and not self.left_pressed and not self.right_pressed:
                if os.path.exists(up_image_placeholder):
                    up_image = pygame.image.load(up_image_placeholder)
                    self.screen.blit(up_image,(self.playerx,self.playery))
                else:
                    self.screen.blit(self.player_img, (self.playerx, self.playery))
            elif self.down_pressed and not self.left_pressed and not self.right_pressed:
                if os.path.exists(down_image_placeholder):
                    down_image = pygame.image.load(down_image_placeholder)
                    self.screen.blit(down_image,(self.playerx,self.playery))
                else:
                    self.screen.blit(self.player_img, (self.playerx, self.playery))
            else:
                self.screen.blit(self.player_img, (self.playerx, self.playery))
        else:
            self.screen.blit(self.player_img, (self.playerx, self.playery))

    # creating an enemy
    def create_enemy(self,image_path,org=(370,40)):
        self.enemy_image_path = image_path
        self.enemyx, self.enemyy = org
        self.enemy_img = pygame.image.load(image_path)
        self.enemy_width, self.enemy_height = self.enemy_img.get_size()

    # loading an enemy
    def load_enemy(self):
        if self.is_lr_mapped_to_enemy:
            # checking if there are other images for each keystroke
            pathname = os.path.dirname(self.enemy_image_path)
            image_name = self.enemy_image_path.split("/")[-1]
            image_name_wo_ext = image_name.split(".")[0]  # without extension
            image_ext = image_name.split(".")[-1]
            left_image_placeholder = pathname + '/' + image_name_wo_ext + "_left" + "." + image_ext
            up_left_image_placeholder = pathname + '/' + image_name_wo_ext + "_up_left" + "." + image_ext
            down_left_image_placeholder = pathname + '/' + image_name_wo_ext + "_down_left" + "." + image_ext
            right_image_placeholder = pathname + '/' + image_name_wo_ext + "_right" + "." + image_ext
            up_right_image_placeholder = pathname + '/' + image_name_wo_ext + "_up_right" + "." + image_ext
            down_right_image_placeholder = pathname + '/' + image_name_wo_ext + "_down_right" + "." + image_ext
            up_image_placeholder = pathname + '/' + image_name_wo_ext + "_up" + "." + image_ext
            down_image_placeholder = pathname + '/' + image_name_wo_ext + "_down" + "." + image_ext
            # checking for keystrokes
            if self.left_pressed and self.up_pressed:
                if os.path.exists(up_left_image_placeholder):
                    up_left_image = pygame.image.load(up_left_image_placeholder)
                    self.screen.blit(up_left_image, (self.enemyx, self.enemyy))
            elif self.left_pressed and self.down_pressed:
                if os.path.exists(down_left_image_placeholder):
                    down_left_image = pygame.image.load(down_left_image_placeholder)
                    self.screen.blit(down_left_image, (self.enemyx, self.enemyy))
            elif self.left_pressed and not self.up_pressed and not self.down_pressed:
                if os.path.exists(left_image_placeholder):
                    left_image = pygame.image.load(left_image_placeholder)
                    self.screen.blit(left_image, (self.enemyx, self.enemyy))
                else:
                    self.screen.blit(self.enemy_img, (self.enemyx, self.enemyy))
            elif self.right_pressed and self.up_pressed:
                if os.path.exists(up_right_image_placeholder):
                    up_right_image = pygame.image.load(up_right_image_placeholder)
                    self.screen.blit(up_right_image, (self.enemyx, self.enemyy))
            elif self.right_pressed and self.down_pressed:
                if os.path.exists(down_right_image_placeholder):
                    down_right_image = pygame.image.load(down_right_image_placeholder)
                    self.screen.blit(down_right_image, (self.enemyx, self.enemyy))
            elif self.right_pressed and not self.up_pressed and not self.down_pressed:
                if os.path.exists(right_image_placeholder):
                    right_image = pygame.image.load(right_image_placeholder)
                    self.screen.blit(right_image, (self.enemyx, self.enemyy))
                else:
                    self.screen.blit(self.enemy_img, (self.enemyx, self.enemyy))
            elif self.up_pressed and not self.left_pressed and not self.right_pressed:
                if os.path.exists(up_image_placeholder):
                    up_image = pygame.image.load(up_image_placeholder)
                    self.screen.blit(up_image, (self.enemyx, self.enemyy))
                else:
                    self.screen.blit(self.enemy_img, (self.enemyx, self.enemyy))
            elif self.down_pressed and not self.left_pressed and not self.right_pressed:
                if os.path.exists(down_image_placeholder):
                    down_image = pygame.image.load(down_image_placeholder)
                    self.screen.blit(down_image, (self.enemyx, self.enemyy))
                else:
                    self.screen.blit(self.enemy_img, (self.enemyx, self.enemyy))
            else:
                self.screen.blit(self.enemy_img, (self.enemyx, self.enemyy))
        else:
            self.screen.blit(self.enemy_img, (self.enemyx, self.enemyy))

    # creating an object
    def create_object(self,image_path,org=(370,240)):
        self.object_image_path = image_path
        self.objectx, self.objecty = org
        self.object_img = pygame.image.load(image_path)
        self.object_width, self.object_height = self.object_img.get_size()

    # loading an object
    def load_object(self):
        if self.is_lr_mapped_to_object:
            # checking if there are other images for each keystroke
            pathname = os.path.dirname(self.object_image_path)
            image_name = self.object_image_path.split("/")[-1]
            image_name_wo_ext = image_name.split(".")[0]  # without extension
            image_ext = image_name.split(".")[-1]
            left_image_placeholder = pathname + '/' + image_name_wo_ext + "_left" + "." + image_ext
            up_left_image_placeholder = pathname + '/' + image_name_wo_ext + "_up_left" + "." + image_ext
            down_left_image_placeholder = pathname + '/' + image_name_wo_ext + "_down_left" + "." + image_ext
            right_image_placeholder = pathname + '/' + image_name_wo_ext + "_right" + "." + image_ext
            up_right_image_placeholder = pathname + '/' + image_name_wo_ext + "_up_right" + "." + image_ext
            down_right_image_placeholder = pathname + '/' + image_name_wo_ext + "_down_right" + "." + image_ext
            up_image_placeholder = pathname + '/' + image_name_wo_ext + "_up" + "." + image_ext
            down_image_placeholder = pathname + '/' + image_name_wo_ext + "_down" + "." + image_ext
            # checking for keystrokes
            if self.left_pressed and self.up_pressed:
                if os.path.exists(up_left_image_placeholder):
                    up_left_image = pygame.image.load(up_left_image_placeholder)
                    self.screen.blit(up_left_image, (self.objectx, self.objecty))
            elif self.left_pressed and self.down_pressed:
                if os.path.exists(down_left_image_placeholder):
                    down_left_image = pygame.image.load(down_left_image_placeholder)
                    self.screen.blit(down_left_image, (self.objectx, self.objecty))
            elif self.left_pressed and not self.up_pressed and not self.down_pressed:
                if os.path.exists(left_image_placeholder):
                    left_image = pygame.image.load(left_image_placeholder)
                    self.screen.blit(left_image, (self.objectx, self.objecty))
                else:
                    self.screen.blit(self.object_img, (self.objectx, self.objecty))
            elif self.right_pressed and self.up_pressed:
                if os.path.exists(up_right_image_placeholder):
                    up_right_image = pygame.image.load(up_right_image_placeholder)
                    self.screen.blit(up_right_image, (self.objectx, self.objecty))
            elif self.right_pressed and self.down_pressed:
                if os.path.exists(down_right_image_placeholder):
                    down_right_image = pygame.image.load(down_right_image_placeholder)
                    self.screen.blit(down_right_image, (self.objectx, self.objecty))
            elif self.right_pressed and not self.up_pressed and not self.down_pressed:
                if os.path.exists(right_image_placeholder):
                    right_image = pygame.image.load(right_image_placeholder)
                    self.screen.blit(right_image, (self.objectx, self.objecty))
                else:
                    self.screen.blit(self.object_img, (self.objectx, self.objecty))
            elif self.up_pressed and not self.left_pressed and not self.right_pressed:
                if os.path.exists(up_image_placeholder):
                    up_image = pygame.image.load(up_image_placeholder)
                    self.screen.blit(up_image, (self.objectx, self.objecty))
                else:
                    self.screen.blit(self.object_img, (self.objectx, self.objecty))
            elif self.down_pressed and not self.left_pressed and not self.right_pressed:
                if os.path.exists(down_image_placeholder):
                    down_image = pygame.image.load(down_image_placeholder)
                    self.screen.blit(down_image, (self.objectx, self.objecty))
                else:
                    self.screen.blit(self.object_img, (self.objectx, self.objecty))
            else:
                self.screen.blit(self.object_img, (self.objectx, self.objecty))
        else:
            self.screen.blit(self.object_img, (self.objectx, self.objecty))

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

    # bounding a character to the window
    def bound_character_to_window(self,obj):
        if obj.ypos < 0:
            obj.ypos = 0
        if obj.ypos > self.wheight - obj.height:
            obj.ypos = self.wheight - obj.height
        if obj.xpos < 0:
            obj.xpos = 0
        if obj.xpos > self.wwidth - obj.width:
            obj.xpos = self.wwidth - obj.width

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
            if self.playery == self.wheight-self.player_height:
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

    # bouncing up and down
    def bounce_up_down(self,type="enemy",speed=1):
        edge = self.detect_edge(type=type)

        if edge == "top":
            self.move_top_to_bottom(type=type, speed=speed)
        elif edge == "bottom":
            self.move_bottom_to_top(type=type, speed=speed)
        else:
            self.move_top_to_bottom(type=type, speed=speed)

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
        self.random_xlimit = xlimit
        self.random_ylimit = ylimit
        lower_xlimit, upper_xlimit = self.random_xlimit
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
        score_font = pygame.font.SysFont("comicsansms", 20)
        score_text = score_font.render("Score : " + str(score), True, (255, 255, 255))
        score_rect = score_text.get_rect()
        score_rect.center = (self.wwidth/2-300, 40)
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
        if type == "death":
            self.death_sound_path = pygame.mixer.Sound(sound_path)
            self.death_sound_volume = volume
            self.death_sound_activated = True
        if type == "victory":
            self.victory_sound_path = pygame.mixer.Sound(sound_path)
            self.victory_sound_volume = volume
            self.victory_sound_activated = True

    # update max lives
    def update_max_lives(self,max_lives=3):
        self.max_lives = max_lives

    # decrease life
    def decrease_life(self):
        self.lives -= 1
        # checking for sound in trigger and activating it
        if self.death_sound_activated:
            self.death_sound = pygame.mixer.Sound(self.death_sound_path)
            self.death_sound.set_volume(self.death_sound_volume)
            self.death_sound.play()

    # increase life
    def increase_life(self):
        self.lives += 1

    # display lives
    def display_lives(self,score=0):
        life = self.lives
        life_font = pygame.font.SysFont("comicsansms", 20)
        life_text = life_font.render("Lives : " + str(life), True, (255, 255, 255))
        life_rect = life_text.get_rect()
        life_rect.center = (self.wwidth/2-300, 70)
        self.screen.blit(life_text, life_rect)

    # game over
    def game_over(self,text="GAME OVER",font="comicsansms",font_size=100,color=(255,0,0)):
        print("GAME OVER")
        gameover_font = pygame.font.SysFont(font,font_size)
        gameover_text = gameover_font.render(text, True, color)
        gameover_rect = gameover_text.get_rect()
        gameover_rect.center = (self.wwidth/2, self.wheight/2)
        self.screen.blit(gameover_text, gameover_rect)
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        # Update the display after rendering
        pygame.display.update()
        # killing the program
        self.game_over_state = True
        while self.game_over_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over_state = False  # Exit the pause loop without quitting the application

    # game over
    def you_won(self, text="You Won!", font="comicsansms", font_size=100, color=(255, 0, 0)):
        print("You Won!")
        gameover_font = pygame.font.SysFont(font, font_size)
        gameover_text = gameover_font.render(text, True, color)
        gameover_rect = gameover_text.get_rect()
        gameover_rect.center = (self.wwidth / 2, self.wheight / 2)
        self.screen.blit(gameover_text, gameover_rect)
        pygame.mixer.music.stop()
        pygame.mixer.stop()
        # Update the display after rendering
        pygame.display.update()
        # killing the program
        self.game_over_state = True
        while self.game_over_state:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over_state = False  # Exit the pause loop without quitting the application

    # drawing text
    def draw_text(self,text="your text here",font="comicsansms",font_size=20,color=(255,255,255),xpos=0,ypos=0):
        font = pygame.font.SysFont(font, font_size)
        text = font.render(text, True, color)
        text_rect = text.get_rect()
        text_rect.topleft = (xpos, ypos)
        self.screen.blit(text, text_rect)

    # tranformations
    def transform(self,type="player",style="flip_horizontally",angle=None,factor=None):
        transformed_img = None  # setting local variable
        if type == "player":
            if style == "flip_horizontally":
                transformed_img = pygame.transform.flip(self.player_img, True, False)
                self.player_transformed = True
            elif style == "flip_vertically":
                transformed_img = pygame.transform.flip(self.player_img, False, True)
                self.player_transformed = True
            elif style == "rotate":
                if angle is None:
                    print("angle not specified")
                    return
                transformed_img = pygame.transform.rotate(self.player_img, angle)
                self.player_transformed = True
            elif style == "scale":
                if factor is None:
                    print("scaling factor not specified")
                    return
                new_width = int(self.player_img.get_width() * factor)
                new_height = int(self.player_img.get_height() * factor)
                transformed_img = pygame.transform.smoothscale(self.player_img, (new_width, new_height))
            else:
                print("incorrect style option")
        self.screen.blit(transformed_img, (self.playerx, self.playery))
        pygame.display.flip()

    # setting the fps of the screen
    def set_fps(self,fps=60):
        self.fps = fps

    # setting a delay on the screen(in seconds
    def delay_screen_refresh(self,delay=1):
        # turning milliseconds to seconds
        delay = delay*1000
        pygame.time.wait(int(delay))

    # drawing a line
    def draw_line(self,start=(0,0),end=(0,0),color=(255,255,255),width=1):
        pygame.draw.line(self.screen, color, start, end, width)

    # drawing a rect
    def draw_rect(self,color=(255,255,255),org=(50,50),width=100,height=100,border_thickness=0,border_radius=0):
        xpos, ypos = org
        rect = (xpos,ypos,width,height)
        pygame.draw.rect(self.screen, color=color, rect=rect, width=border_thickness, border_radius=border_radius)

    # drawing an arc
    def draw_arc(self,color=(255,255,255),org=(10,10),width=100,height=100,start_angle=0,stop_angle=90,border_thickness=0):
        rect = (org[0],org[1],width,height)
        start_angle = math.radians(start_angle) # for clockwise start_angle must be bigger than stop_angle
        stop_angle = math.radians(stop_angle)   # for anti-clockwise start_angle must be smaller than stop_angle
        pygame.draw.arc(self.screen, color=color, rect=rect, start_angle=start_angle, stop_angle=stop_angle, width=border_thickness)

    # drawing a polygon
    def draw_polygon(self,color=(255,255,255),points=None,border_thickness=0):
        if points is None:
            print("points not specified")
            return
        pygame.draw.polygon(self.screen, color=color, points=points, width=border_thickness)

    # giving a random integer number
    def random_number(self,start=0,end=10):
        return random.randint(start,end)

    # giving a random color
    def random_color(self):
        color = ()
        color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        return color

    # detecting collision between two characters
    def detect_character_collision(self,obj1, obj2):
        return (
                obj1.xpos < obj2.xpos + obj2.width and
                obj1.xpos + obj1.width > obj2.xpos and
                obj1.ypos < obj2.ypos + obj2.height and
                obj1.ypos + obj1.height > obj2.ypos
        )

    # saving highest score
    def save_highest_score(self,score=0):
        with open(self.HIGH_SCORE_FILE,"w") as file:
            file.write(str(score))

    # loading highest score
    def load_highest_score(self):
        if os.path.exists(self.HIGH_SCORE_FILE):
            with open(self.HIGH_SCORE_FILE,"r") as file:
                return int(file.read())
        return 0 # if the file doesn't exist

    # a new class for characters
    class character:
        def __init__(self, parent, type="shape", image_path="image_path", character_shape="rectangle", color=(255, 0, 0), org=(0, 0), width=30,
                     height=30, border_thickness=0, border_radius=0):
            self.parent = parent
            self.type = type
            self.image_path = image_path
            self.image = None
            self.image_rect = None
            self.character_shape = character_shape
            self.color = color
            self.xpos, self.ypos = org
            self.width = width
            self.height = height
            self.border_thickness = border_thickness
            self.border_radius = border_radius

            # initial values
            self.speed = 1

            # state of the object
            self.alive = True

        def __del__(self):
            self.alive = False

        def check_vitals(self):
            if not self.alive:
                raise Exception("Character is dead")

        def load(self):
            self.check_vitals()
            if self.type == "image":
                self.image = pygame.image.load(self.image_path)
                self.image_rect = self.image.get_rect()
                self.parent.screen.blit(self.image,(self.xpos,self.ypos))
            elif self.type == "shape":
                if self.character_shape == "rectangle":
                    player = self.parent.draw_rect(color=self.color, org=(self.xpos, self.ypos), width=self.width,
                                                   height=self.height, border_thickness=self.border_thickness,
                                                   border_radius=self.border_radius)

        def change_position(self, xpos, ypos):
            self.check_vitals()
            if self.type == "image":
                self.image_rect.xpos, self.image_rect.ypos = xpos,ypos
            if self.character_shape == "rectangle":
                self.xpos = xpos
                self.ypos = ypos

        def change_shape(self, width, height):
            self.check_vitals()
            if self.character_shape == "rectangle":
                self.width = width
                self.height = height

        def move_left(self):
            self.check_vitals()
            self.xpos -= 10

        def move_right(self, speed=None):
            self.check_vitals()
            if speed:
                self.speed = speed
            self.xpos += self.speed

        def find_position(self):
            self.check_vitals()
            return self.xpos, self.ypos

        def update_position(self, xpos=None, ypos=None):
            self.check_vitals()
            if self.type == "image":
                self.xpos, self.ypos = xpos,ypos
            if self.type == "shape":
                if self.character_shape == "rectangle":
                    if xpos is not None:
                        self.xpos = xpos
                    if ypos is not None:
                        self.ypos = ypos

        def update_shape(self, width=None, height=None):
            self.check_vitals()
            if width is not None:
                self.width = width
            if height is not None:
                self.height = height

        def update_speed(self, speed=None):
            self.check_vitals()
            if speed is not None:
                self.speed = speed

        def update_border_thickness(self, thickness=None):
            self.check_vitals()
            if thickness is not None:
                self.border_thickness = thickness

        def update_border_radius(self, radius=None):
            self.check_vitals()
            if radius is not None:
                self.border_radius = radius

        def update_color(self, color=None):
            self.check_vitals()
            if color is not None:
                self.color = color

        def kill(self):
            self.__del__()