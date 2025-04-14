'''
@author: Sudip Vikram Adhikari
@company: Beyond Apogee
NOTE: This is a game canvas for a more decorated crossy road game.
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

# multiple vehicles
vehicles = []

# let's have 5 vehicles moving at any given time
for i in range(5):
    vehicle = game.character(parent=game,type="object",player_shape="rectangle",
                             color=game.random_color(),
                             org=(0, game.random_number(100, game.wheight - 100)),
                             width=game.random_number(50,100),
                             height=game.random_number(10,50),border_thickness=0,
                             border_radius=game.random_number(0,5))
    vehicles.append(vehicle)

while True:
    game.background_color(color=(0,0,0))
    # drawing the edges of road # green patches
    game.draw_rect(color=(0,255,0),xpos=0,ypos=0,width=game.wwidth,height=50,border_thickness=0)
    game.draw_rect(color=(0,255,0),xpos=0,ypos=game.wheight-50,width=game.wwidth,height=50,border_thickness=0)
    # loading characters
    chicken.load()

    # loading the vehicles
    for i, vehicle in enumerate(vehicles):
        if vehicle.alive:
            vehicle.load()
            vehicle.move_right(game.random_number(1,5))

            if vehicle.xpos > game.wwidth:
                vehicle.kill()
                vehicle = game.character(parent=game, type="object", player_shape="rectangle",
                                         color=game.random_color(),
                                         org=(0, game.random_number(100, game.wheight-100)),
                                         width=game.random_number(50, 100),
                                         height=game.random_number(10, 50), border_thickness=0,
                                         border_radius=game.random_number(0, 5))
                vehicle.update_speed(speed=game.random_number(1, 5))
                vehicles[i] = vehicle

    # setting frames per second
    game.set_fps(60)
    # refreshing window
    game.refresh_window()