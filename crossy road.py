'''
@author: Sudip Vikram Adhikari
@company: Beyond Apogee
A chicken tries to cross a busy road. The road is multiple lanes and there are lots
of vehicles. You are the chicken and your mission is to successfully navigate around
the vehicles and cross the road, unless you want to end up becoming a road kill.
'''

from sajilopygame import *

# initiatilizing the class
game = sajilopygame(wwidth=600,wheight=500)

# changing title of the game window
game.window_title("Crossy Road")

# creating characters
chicken = game.character(parent=game,type="player",player_shape="rectangle",color=(0,255,0),org=(10,10),width=30,height=30,border_thickness=0,border_radius=0)
vehicle = game.character(parent=game,type="object",player_shape="rectangle",color=(255,0,100),org=(0,100),width=80,height=30,border_thickness=0,border_radius=0)

# multiple vehicles
vehicles = []
vehicles.append(vehicle)

while True:
    game.background_color(color=(0,0,0))
    # loading characters
    chicken.load()

    # let's have 5 vehicles moving at any given time
    for i in range(5):
        vehicle.load()
        vehicle.move_right(5)

    # setting frames per second
    game.set_fps(60)
    # refreshing window
    game.refresh_window()