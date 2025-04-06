from sajilopygame import sajilopygame

game = sajilopygame()
game.window_title("Space Invaders")
game.favicon("ufo.png")

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

    # map left and right keystrokes to a player
    game.map_lr_keys_to_player(intensity=(5,6))
    # map up and down keystrokes to a player
    game.map_ud_keys_to_player(intensity=(6,5))

    # map left and right keystrokes to an enemy
    game.map_lr_keys_to_enemy(intensity=(4,3))
    # map up and down keystrokes to an enemy
    game.map_ud_keys_to_enemy(intensity=(4,3))

    # map left and right keystrokes to an object
    game.map_lr_keys_to_object(intensity=(2,4))
    # map up and down keystrokes to an object
    game.map_ud_keys_to_object(intensity=(6,3))

    # getting the position of player
    pposition = game.find_player_position()
    print(pposition)
    eposition = game.find_enemy_position()
    print(eposition)
    oposition = game.find_object_position()
    print(oposition)

    # getting the width and height of players, enemies and objects
    player_width, player_height = game.find_player_size()
    enemy_width, enemy_height = game.find_enemy_size()
    object_width, object_height = game.find_object_size()
    print(f"player width: {player_width} and height: {player_height}")
    print(f"enemy width: {enemy_width} and height: {enemy_height}")
    print(f"object width: {object_width} and height: {object_height}")

    # animating the enemy
    game.move_left_to_right(type="enemy",speed=5)
    game.move_right_to_left(type="player",speed=5)
    game.move_left_to_right(type="object",speed=5)

    # edge detection and bounce
    edge = game.detect_edge(type="enemy")
    print(edge)
    print(game.find_enemy_position())
    '''
    from left to right and right to left
    if edge == "left":
        game.move_left_to_right(type="enemy",speed=5)
    elif edge == "right":
        game.move_right_to_left(type="enemy",speed=5)
    else:
        game.move_left_to_right(type="enemy",speed=5)
    from top to bottom and bottom to top
    if edge == "top":
        game.move_top_to_bottom(type="enemy",speed=5)
    elif edge == "bottom":
        game.move_bottom_to_top(type="enemy",speed=5)
    else:
        game.move_top_to_bottom(type="enemy",speed=5)'''
    # mapping keystrokes to the player
    game.map_lr_keys(type="player",intensity=(5,5))

    # bouncing from left to right
    game.bounce_left_right(type="enemy",speed=5)
    game.bounce_top_bottom(type="player",speed=5)

    # bounding the player to the window
    game.bound_player_to_window()
    game.bound_enemy_to_window()
    game.bound_object_to_window()

    game.refresh_window()
