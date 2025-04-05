from sajilopygame import sajilopygame

game = sajilopygame()
game.window_title("Space Invaders")
game.favicon("ufo.png")

while True:
    game.background_color((255, 255, 255))
    game.background_image('background.png')

    # creating a player
    game.player(image_path="spaceship.png",org=(370,480))

    game.refresh_window()
