'''
@author: Sudip Vikram Adhikari
@company: Beyond Apogee
This is the classic car race game, where you are the driver trying to move out of the way of
incoming cars. Every car you avoid gains you a score.
'''

from sajilopygame import *

# initializing the class
game = sajilopygame(wwidth=400, wheight=500)

# changing title
game.window_title("Racing Car Game")

# creating the player car
player_car = game.character(parent=game,type="shape",character_shape="rectangle",
                            color=(255,255,0),org=(180,350),width=30,height=60)

# manually creating two cars side by side
left_side_car = game.character(parent=game,type="shape",character_shape="rectangle",
                               color=(255,0,0),org=(100,350),width=30,height=60)
right_side_car = game.character(parent=game,type="shape",character_shape="rectangle",
                                color=(0,0,255),org=(200,350),width=30,height=60)

while True:
    game.background_color((0,0,0))
    # loading the player car
    player_car.load()

    game.refresh_window()