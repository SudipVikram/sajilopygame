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
    game.map_lr_keys_to_player(intensity=5)
    # map up and down keystrokes to a player
    game.map_ud_keys_to_player(intensity=5)

    # map left and right keystrokes to an enemy
    game.map_lr_keys_to_enemy(intensity=5)
    # map up and down keystrokes to an enemy
    game.map_ud_keys_to_enemy(intensity=5)

    game.refresh_window()
