'''
@author: Sudip Vikram Adhikari
@company: Beyond Apogee
This game idea has been borrowed from the following website:
https://www.youtube.com/watch?v=FfWpgLFMI7w
The assets and characters have been taken from the above website.
'''

from sajilopygame import sajilopygame

# initializing with default window dimensions
game = sajilopygame()

# window title and icon
game.window_title("Space Invaders")
game.favicon("assets/ufo.png")

# creating game characters
game.create_player(image_path="assets/spaceship.png", org=(370, 480))
game.create_enemy(image_path="assets/alien.png", org=(370, 40))
game.create_object(image_path="assets/bullet.png", org=(370 + 16, 480 + 10))

# loading sounds
game.load_sound(sound_path="assets/background.wav", type="background", volume=0.5)
game.load_sound(sound_path="assets/explosion.wav", type="collision", volume=1)
game.load_sound(sound_path="assets/laser.wav", type="trigger", volume=0.5)
game.load_sound(sound_path="assets/explosion.wav", type="death", volume=0.5)

while True:
    # background color and image for the window
    game.background_color((255, 255, 255))
    game.background_image('assets/background.png')

    # loading characters
    game.load_object()
    game.load_player()
    game.load_enemy()

    # assigning keystrokes to the player
    game.assign_lr_keys(type="player",intensity=(5,5))

    # bouncing left and right
    game.bounce_left_right(type="enemy",speed=5)

    # finding enemy position
    enemy_xpos, enemy_ypos = game.find_position(type="enemy")

    # if the enemy is on either edges we will move it one step below
    if enemy_xpos <= 0 or enemy_xpos >= 736:
        game.update_position(type="enemy",xpos=enemy_xpos,ypos=enemy_ypos+30)

    # binding the object's position with the player's
    player_pos = game.find_position(type="player")

    # updating the object's position
    x,y = player_pos
    x = x+16
    y = y+25

    # assigning the trigger  # setup to fire bullets upon trigger press
    game.assign_trigger(type="object",start_pos=(x,y),dir="b2t",speed=50)

    # assign collision effect
    game.assign_collision_effect(type="object",effect="disappear")
    game.assign_collision_effect(type="enemy", effect="random")

    # detect collision
    game.detect_collision(collision_by="object",collision_with="enemy")

    # limiting the randomness
    game.limit_randomness(type="enemy",xlimit=(0,0),ylimit=(0,450))

    # displaying the scoreboard
    game.display_score()

    # checking for lives # if the enemy comes near
    ypos = game.find_position(type="enemy")[1]
    if ypos >= 400:
        game.decrease_life()
        game.move_to_random(type="enemy")

    # displaying the remaining lives of player
    game.display_lives()

    # bounding the characters to the window
    game.bound_to_window(type="player")
    game.bound_to_window(type="enemy")

    # reload the frame
    game.refresh_window()
