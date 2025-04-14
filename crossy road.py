from sajilopygame import *

game = sajilopygame(wwidth=600,wheight=500)

game.window_title("Crossy Road")

chicken = game.character(parent=game,type="player",player_shape="rectangle",color=(0,255,0),org=(10,10),width=30,height=30,border_thickness=0,border_radius=0)

#list of all vehicles
vehicles = []
vehicle = game.character(parent=game,type="object",player_shape="rectangle",color=(255,0,100),org=(0,100),width=80,height=30,border_thickness=0,border_radius=0)
vehicle_2 = game.character(parent=game,type="object",player_shape="rectangle",color=(0,255,50),org=(0,200),width=100,height=30,border_thickness=0,border_radius=0)
#vehicles.append(vehicle_1)

while True:
    game.background_color(color=(0,0,0))
    chicken.load()

    if vehicle.alive:
        vehicle.load()
        vehicle.move_right(5)

        if vehicle.xpos > game.wwidth:
            vehicle.kill()

            # spawning
            vehicle = game.character(parent=game,type="object",player_shape="rectangle",color=(255,0,100),org=(0,100),width=80,height=30,border_thickness=0,border_radius=0)
            vehicle.update_position(
                xpos=0,
                ypos=random.randint(0,game.wheight))
            vehicle.update_speed(speed=random.randint(4,10))
            vehicle.update_color(
                color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            vehicle.update_shape(
                width=random.randint(50,100),
                height=random.randint(10,50))


    '''if vehicle_1.alive:
        vehicle_1.load()
        vehicle_1.update_speed(5)
    #vehicle_2.load()

    # loop through all vehicles
    for i, vehicle in enumerate(vehicles):
        if vehicle.alive:
            #print(f"Vehicle {i} is alive")
            vehicle.load()
            vehicle.move_right()
        if vehicle.xpos > game.wwidth:
            vehicle.kill()
            print(f"Vehicle {i} is killed. Spawning another character")

            #spawn a new vehicle and replace the dead one
            new_vehicle = character(parent=game,type="object",player_shape="rectangle",color=(255,0,100),org=(0,100),width=80,height=30,border_thickness=0,border_radius=0)
            vehicles[i] = new_vehicle
            new_vehicle.update_position(
                xpos=0,
                ypos=random.randint(0,game.wheight))
            new_vehicle.update_speed(speed=random.randint(4,10))
            new_vehicle.update_color(
                color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
            new_vehicle.update_shape(
                width=random.randint(50,100),
                height=random.randint(10,50))'''

    game.set_fps(60)
    game.refresh_window()