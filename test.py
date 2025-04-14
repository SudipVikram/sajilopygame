from sajilopygame import *

game = sajilopygame(wwidth=400,wheight=400)

game.window_title("Testing new features out")

game.create_player("./astronaut.png",org=(140,140))

while True:
    game.background_color(color=(0,0,0))
    #game.load_player()

    #game.assign_lr_keys(type="player",intensity=(1,1))
    #game.assign_ud_keys(type="player",intensity=(1,1))

    # transforming the orientation of the player
    #game.transform(type="player", style="flip_horizontally")
    #game.transform(type="player",style="flip_vertically")
    #game.transform(type="player", style="rotate", angle=45)
    #game.transform(type="player", style="scale", factor=2)

    #game.bounce_left_right(type="player",speed=5)

    #game.bound_to_window(type="player")

    # drawing
    game.draw_arc(color=(0,0,255),org=(10,10),start_angle=0,stop_angle=180,border_thickness=1)
    game.draw_line(start=(200,0),end=(400,400),color=(255,0,0),width=5)
    game.draw_line(start=(400,400),end=(0,0),color=(0,255,0),width=1)
    game.draw_rect(color=(255,255,0),xpos=100,ypos=100,width=100,height=250,border_thickness=0,border_radius=5)
    game.draw_polygon(color=(255,0,100),points=((100,100),(200,200),(300,100),(400,150)),border_thickness=0)

    game.set_fps(fps=60)
    game.refresh_window()