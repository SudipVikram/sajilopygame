'''
@author: Sudip Vikram Adhikari
@company: Beyond Apogee
There are a lot of geese flying around. The geese seem to drop their eggs as they fly about.
A clever farmer is trying his luck by catching the eggs. Let's see how many eggs you can catch.
This program uses the concept of initializing one class with many objects.
'''

from sajilopygame import *

# creating instances of sajilopygame
game = sajilopygame()
goose2 = sajilopygame()
goose3 = sajilopygame()

# one time settings for sajilopygame
game.window_title("Catch the Eggs")

# creating characters for the game
game.create_player(image_path="assets/basket.png", org=(370, 400))
game.create_object(image_path="assets/egg.png", org=(100, 100))
game.create_enemy(image_path="assets/duck.png", org=(400, 10))
goose2.create_enemy(image_path="assets/duck.png", org=(400, 10))
goose3.create_enemy(image_path="assets/duck.png", org=(400, 10))

# working with sounds
game.load_sound(sound_path="assets/background.wav", type="background", volume=0.5)
game.load_sound(sound_path="assets/egg-in-basket.wav", type="collision", volume=0.5)

while True:
    # loading for game
    game.background_image(image_path="assets/background.jpg")
    game.load_player()
    game.load_object()
    game.load_enemy()
    goose2.load_enemy()
    goose3.load_enemy()

    # assigning game keys
    game.assign_lr_keys(type="player",intensity=(20,20))

    # moving the geese left to right
    game.move_right_to_left(type="enemy",speed=random.randint(5,10))
    goose2.move_right_to_left(type="enemy",speed=random.randint(5,10))
    goose3.move_right_to_left(type="enemy",speed=random.randint(5,10))
    # finding the position of the enemy, which is the main goose
    ex, ey = game.find_position(type="enemy")
    # once it goes out of bounds    # checking for edge
    if ex<0:
        game.update_position(type="enemy",xpos=900, ypos=random.randint(5,150))     # randomising the y-axis position
    # repeating for the other two goose
    ex2, ey2 = goose2.find_position(type="enemy")
    # once it goes out of bounds
    if ex2 < 0:
        goose2.update_position(type="enemy", xpos=900, ypos=random.randint(5, 150))
    ex3, ey3 = goose3.find_position(type="enemy")
    # once it goes out of bounds
    if ex3 < 0:
        game.update_position(type="enemy", xpos=900, ypos=random.randint(5, 150))

    # moving the object left to right  # object here meaning the egg
    game.move_top_to_bottom(type="object",speed=10)
    ox, oy = game.find_position(type="object")
    # once it goes out of bounds
    if oy>game.wheight:
        game.update_position(type="object",xpos=random.randint(50,900), ypos=0)

    # collision detection
    # assign collision effect
    game.assign_collision_effect(type="object", effect="disappear")

    # detect collision
    game.detect_collision(collision_by="object",collision_with="player")

    # display the scoreboard
    game.display_score()

    # bounding the basket
    game.bound_to_window(type="player")

    # bare essentials
    game.refresh_window()