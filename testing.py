from sajilopygame import sajilopygame

game = sajilopygame()
#game2 = sajilopygame()
game.window_title("Space Invaders")
game.favicon("assets/ufo.png")
state = "hold"

# need to work on the commits(just a comment)
# creating an object bullet
game.create_object(image_path="assets/bullet.png", org=(370 + 16, 480 + 10))
#game2.create_object(image_path="assets/bullet.png", org=(370 + 16, 480 + 10))
# creating a player
game.create_player(image_path="assets/spaceship.png", org=(370, 480))
# creating an enemy
game.create_enemy(image_path="assets/alien.png", org=(370, 40))
#game2.create_enemy(image_path="assets/monster.png", org=(370, 40))

# working with sounds
game.load_sound(sound_path="assets/background.wav",type="background",volume=0.5)
game.load_sound(sound_path="assets/explosion.wav", type="collision", volume=1)
game.load_sound(sound_path="assets/laser.wav", type="trigger", volume=0.5)
game.load_sound(sound_path="assets/explosion.wav", type="death", volume=0.5)

while True:
    game.background_color((255, 255, 255))
    game.background_image('assets/background.png')
    game.load_object()
    #game2.load_object()
    game.load_player()
    game.load_enemy()
    #game2.load_enemy()

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
    #game2.bounce_left_right(type="enemy",speed=10)

    enemy_xpos, enemy_ypos = game.find_position(type="enemy")
    if enemy_xpos <= 0 or enemy_xpos >= 736:
        game.update_position(type="enemy",xpos=enemy_xpos,ypos=enemy_ypos+30)
    #enemy_xpos2, enemy_ypos2 = game2.find_position(type="enemy")
    #if enemy_xpos2 <= 0 or enemy_xpos2 >= 736:
        #game2.update_position(type="enemy", xpos=enemy_xpos2, ypos=enemy_ypos2 + 30)

    # always setting the player to the object
    player_pos = game.find_position(type="player")
    # updating the object's position
    x,y = player_pos
    x = x+16
    y = y+25
    #game.update_object_position(x,y)

    # for firing the bullet
    # assigning the trigger
    game.assign_trigger(type="object",start_pos=(x,y),dir="b2t",speed=50)
    #game2.assign_trigger(type="object",start_pos=(x,y),dir="b2t",speed=50)

    # assign collision effect
    game.assign_collision_effect(type="object",effect="disappear")
    #game2.assign_collision_effect(type="object",effect="disappear")
    game.assign_collision_effect(type="enemy", effect="random")
    #game2.assign_collision_effect(type="enemy", effect="random")
    # detect collision
    game.detect_collision(collision_by="object",collision_with="enemy")
    #game2.detect_collision(collision_by="object", collision_with="enemy")

    # limitint the randomness
    game.limit_randomness(type="enemy",xlimit=(0,0),ylimit=(0,400))

    # displaying the score
    game.display_score()

    # checking for lives
    ypos = game.find_position(type="enemy")[1]
    if ypos >= 400:
        game.decrease_life()
        game.move_to_random(type="enemy")
    # displaying the lives
    game.display_lives()

    # bounding the player to the window
    game.bound_to_window(type="player")
    game.bound_to_window(type="enemy")
    #game2.bound_to_window(type="enemy")
    #game.bound_to_window(type="object")

    game.refresh_window()
