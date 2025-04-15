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
                            color=(255,255,0),org=(180,380),width=30,height=60)

# manually creating two cars side by side
left_lane_car = game.character(parent=game,type="shape",character_shape="rectangle",
                               color=(255,0,0),org=(110,-100),width=30,height=60)
center_lane_car = game.character(parent=game,type="shape",character_shape="rectangle",
                                color=(0,255,255),org=(180,-300),width=30,height=60)
right_lane_car = game.character(parent=game,type="shape",character_shape="rectangle",
                                color=(0,0,255),org=(250,0),width=30,height=60)
# variable for the moving dashes
offset = 0

while True:
    game.background_color((0,0,0))
    # drawing the grass at both sides of the roads
    game.draw_rect(color=(0,255,0),org=(0,0),width=80,height=500)
    game.draw_rect(color=(0,255,0),org=(320,0),width=80,height=500)
    # drawing the edge lines
    game.draw_rect(color=(255,255,0),org=(80,0),width=10,height=500)
    game.draw_rect(color=(255,255,0),org=(310,0),width=10,height=500)

    # drawing the moving dashed lines diving lanes
    for i in range(offset,500,40):
        game.draw_rect(color=(255,255,255),org=(153,i),width=10,height=30)
        game.draw_rect(color=(255, 255, 255), org=(226, i), width=10, height=30)

    # loading the player car
    player_car.load()

    # checking for vitals of our characters
    # left lane car
    if left_lane_car.alive:
        # moving the cars from top to bottom
        left_lane_car.update_position(ypos=left_lane_car.ypos+1)
        left_lane_car.load()
    else:
        left_lane_car = game.character(parent=game,type="shape",character_shape="rectangle",
                               color=(255,0,0),org=(110,game.random_number(-300,-60)),width=30,height=60)
        left_lane_car.load()
    # center lane car
    if center_lane_car.alive:
        center_lane_car.update_position(ypos=center_lane_car.ypos+1)
        center_lane_car.load()
    else:
        center_lane_car = game.character(parent=game,type="shape",character_shape="rectangle",
                                color=(0,255,255),org=(180,game.random_number(-300,-60)),width=30,height=60)
        center_lane_car.load()
    # right lane car
    if right_lane_car.alive:
        right_lane_car.update_position(ypos=right_lane_car.ypos+1)
        right_lane_car.load()
    else:
        right_lane_car = game.character(parent=game,type="shape",character_shape="rectangle",
                                color=(0,0,255),org=(250,game.random_number(-300,-60)),width=30,height=60)
        right_lane_car.load()


    left_lane_car.update_position(ypos=left_lane_car.ypos+1)
    center_lane_car.update_position(ypos=center_lane_car.ypos+1)
    right_lane_car.update_position(ypos=right_lane_car.ypos+1)

    # killing characters if they have exceeded the bottom screen
    if left_lane_car.ypos >= game.wheight:
        left_lane_car.kill()
    if center_lane_car.ypos >= game.wheight:
        center_lane_car.kill()
    if right_lane_car.ypos >= game.wheight:
        right_lane_car.kill()

    # updating the offset to create the motion effect
    offset += 3 # we can change the speed of the dashes by changing this value
    if offset >= 40: # reset the offset
        offset = 0

    game.refresh_window()