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
chicken = game.character(parent=game,type="player",player_shape="rectangle",
                         color=(255,0,0),org=((game.wwidth//2)-30,game.wheight-40),
                         width=30,height=30,border_thickness=0,border_radius=0)

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

# detecting collision
def detect_collision(chicken, vehicle):
    return (
            chicken.xpos < vehicle.xpos + vehicle.width and
            chicken.xpos + chicken.width > vehicle.xpos and
            chicken.ypos < vehicle.ypos + vehicle.height and
            chicken.ypos + chicken.height > vehicle.ypos
    )

# score card
score = 0

# checking for lane crossed
def lane_crossed(chicken):
    global score
    for i, lane_y in enumerate(lanes):
        if lane_y > chicken.ypos:
            score = i
            return 4-score+1

while True:
    game.background_color(color=(0,0,0))
    # drawing the edges of road # green patches
    game.draw_rect(color=(0,255,0),xpos=0,ypos=0,width=game.wwidth,height=50,border_thickness=0)
    game.draw_rect(color=(0,255,0),xpos=0,ypos=game.wheight-50,width=game.wwidth,height=50,border_thickness=0)

    # loading the lanes's margins
    for lane_start in lanes:
        game.draw_line(start=(0,lane_start),end=(game.wwidth,lane_start),color=(255,255,0),width=1)

    # loading characters
    chicken.load()

    # loading the vehicles
    for i, vehicle in enumerate(vehicles):
        if vehicle.alive:
            vehicle.load()
            vehicle.move_right(game.random_number(1,5))

            # check for collisions, if collision kill the chicken, go to game over logic
            if detect_collision(chicken, vehicle):
                chicken.kill()

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

    # checking for road kill
    if not chicken.alive:
        game.game_over(font_size=50)

    # updating the position of the chicken from key presses
    if game.left_pressed:
        chicken.update_position(xpos=chicken.xpos - 1, ypos=chicken.ypos)
    if game.right_pressed:
        chicken.update_position(xpos=chicken.xpos + 1, ypos=chicken.ypos)
    if game.up_pressed:
        chicken.update_position(xpos=chicken.xpos, ypos=chicken.ypos - 1)
    if game.down_pressed:
        chicken.update_position(xpos=chicken.xpos, ypos=chicken.ypos + 1)

    # managing scores in the scoreboard
    scorecard = lane_crossed(chicken)
    if not scorecard:
        scorecard = 0
    game.draw_text(text=f"Score: {scorecard}",xpos=10,ypos=10,color=(255,255,255),font_size=20)

    if scorecard == 5 and chicken.ypos < 10:
        game.you_won(font_size=50,color=(0,255,0))

    # setting frames per second
    game.set_fps(60)
    # refreshing window
    game.refresh_window()