from sajilopygame import sajilopygame

game = sajilopygame()
game.window_title("Space Invaders")
game.favicon("ufo.png")
state = "hold"

# creating an object bullet
game.create_object(image_path="bullet.png", org=(370 + 16, 480 + 10))
# creating a player
game.create_player(image_path="spaceship.png", org=(370, 480))
# creating an enemy
game.create_enemy(image_path="alien.png", org=(370, 40))

while True:
    game.background_color((255, 255, 255))
    game.background_image('background.png')
    game.load_object()
    game.load_player()
    game.load_enemy()

    # assigning keystrokes to the player
    game.assign_lr_keys(type="player",intensity=(5,5))

    # animating the enemy
    #game.move_left_to_right(type="enemy",speed=5)
    #game.move_right_to_left(type="player",speed=5)
    #game.move_left_to_right(type="object",speed=5)

    #game.move_right_to_left(type="enemy",speed=5)
    # detecting edge collision of enemy
    '''edge = game.detect_edge(type="enemy")

    if edge == "left":
        game.move_left_to_right(type="enemy",speed=5)
    elif edge == "right":
        game.move_right_to_left(type="enemy",speed=5)
    else:
        game.move_left_to_right(type="enemy",speed=5)'''

    # bouncing from left to right
    game.bounce_left_right(type="enemy",speed=5)

    enemy_xpos, enemy_ypos = game.find_enemy_position()
    if enemy_xpos <= 0 or enemy_xpos >= 736:
        game.update_enemy_position(enemy_xpos,enemy_ypos+30)

    # always setting the player to the object
    player_pos = game.find_player_position()
    # updating the object's position
    x,y = player_pos
    x = x+16
    y = y+25
    #game.update_object_position(x,y)

    # for firing the bullet
    # assigning the trigger
    game.assign_trigger(type="object",start_pos=(x,y),dir="b2t",speed=50)



    # bounding the player to the window
    game.bound_player_to_window()
    game.bound_enemy_to_window()
    #game.bound_object_to_window()

    game.refresh_window()
