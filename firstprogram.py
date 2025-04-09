from sajilopygame import *

# initializing window
basicgame = sajilopygame(wwidth=800, wheight=600)

# changing widow title and icon
basicgame.window_title("My First Game")
basicgame.favicon("firstgame/favicon.png")

# creating characters
basicgame.create_player("firstgame/astronaut.png")
basicgame.create_enemy("firstgame/monster.png")

while True:
    # changing background parameters
    basicgame.background_color(color=(255, 0, 0))
    basicgame.background_image(image_path="firstgame/background.png")

    # loading characters
    basicgame.load_enemy()
    basicgame.load_player()

    # assigning arrow keys
    basicgame.assign_lr_keys(type="player", intensity=(5, 10))
    basicgame.assign_ud_keys(type="player", intensity=(10, 5))

    # finding enemy's position
    x = basicgame.find_position(type="enemy")[0]

    # update the position of enemy
    # basicgame.update_position(type="enemy",xpos=x,ypos=300)

    # moving enemy from left to right
    basicgame.bounce_left_right(type="enemy", speed=10)

    # collision event
    basicgame.assign_collision_effect(type="enemy", effect="random")
    basicgame.detect_collision(collision_by="player", collision_with="enemy")

    # displaying the scoreboard
    basicgame.display_score()

    # bounding the characters inside window
    basicgame.bound_to_window(type="player")
    basicgame.bound_to_window(type="enemy")

    # refreshing window
    basicgame.refresh_window()