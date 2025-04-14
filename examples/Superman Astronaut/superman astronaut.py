'''
@author: Sudip Vikram Adhikari
@company: Beyond Apogee
This is a simple game to teach students the idea of creating a game using sajilopygame library.
'''

from sajilopygame import *

# initializing window with custom dimensions
game = sajilopygame(wwidth=800, wheight=600)

# widow title and icon
game.window_title("Superman Astronaut")
game.favicon("assets/favicon.png")

# creating characters
game.create_player("assets/astronaut.png")
game.create_enemy("assets/monster.png",org=(0,200))

# loading sounds
game.load_sound(sound_path="assets/gameloop.mp3", type="background", volume=0.5)
game.load_sound(sound_path="assets/happy.mp3", type="collision", volume=0.5)

while True:
    # changing background parameters
    game.background_color(color=(255, 0, 0))
    game.background_image(image_path="assets/background.png")

    # loading characters
    game.load_enemy()
    game.load_player()

    # assigning arrow keys to the player
    game.assign_lr_keys(type="player", intensity=(5, 10))
    game.assign_ud_keys(type="player", intensity=(10, 5))

    # moving the enemy left right up and down in all directions
    game.bounce_left_right(type="enemy", speed=10)
    game.bounce_up_down(type="enemy", speed=10)

    # collision event
    game.assign_collision_effect(type="enemy", effect="random")
    game.detect_collision(collision_by="player", collision_with="enemy")

    # displaying the scoreboard
    game.display_score()

    # bounding the characters inside the window
    game.bound_to_window(type="player")
    game.bound_to_window(type="enemy")

    # reloading frame
    game.refresh_window()