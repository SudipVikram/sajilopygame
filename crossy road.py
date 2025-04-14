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
chicken = game.character(parent=game,type="player",player_shape="rectangle",color=(255,0,0),org=((game.wwidth//2)-30,game.wheight-40),width=30,height=30,border_thickness=0,border_radius=0)

# multiple vehicles
vehicles = []

# multiple lanes
num_lanes = 5   # since there are 5 vehicles
lane_height = (game.wheight - 100) // num_lanes
lanes = [50 + i * lane_height for i in range(num_lanes)]
# i.e., for wheight = 50, lanes = [130,210,290,370,450]

# let's have 5 vehicles moving at any given time
for lane_start in lanes:
    vehicle = game.character(parent=game,type="object",player_shape="rectangle",
                             color=game.random_color(),
                             org=(game.random_number(0,game.wwidth-200), game.random_number(lane_start, lane_start+30)),
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
                                         org=(0, game.random_number(lanes[i], lanes[i]+30)),
                                         width=game.random_number(50, 100),
                                         height=game.random_number(10, 50), border_thickness=0,
                                         border_radius=game.random_number(0, 5))
                vehicle.update_speed(speed=game.random_number(1, 5))
                vehicles[i] = vehicle

    # updating the position of the chicken from key presses
    if game.left_pressed:
        chicken.update_position(xpos=chicken.xpos - 1, ypos=chicken.ypos)
    if game.right_pressed:
        chicken.update_position(xpos=chicken.xpos + 1, ypos=chicken.ypos)
    if game.up_pressed:
        chicken.update_position(xpos=chicken.xpos, ypos=chicken.ypos - 1)
    if game.down_pressed:
        chicken.update_position(xpos=chicken.xpos, ypos=chicken.ypos + 1)

    # setting frames per second
    game.set_fps(60)
    # refreshing window
    game.refresh_window()