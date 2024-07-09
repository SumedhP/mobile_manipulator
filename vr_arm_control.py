from oculus_controller import OculusController
import urx
from math3d.vector import PositionVector
from time import sleep
from math_utils import getMovement

# URX -----
a = 1
v = 0.2

max_movement = 0.5
timeout = 0.25
move_time = 0.4


rob = urx.Robot("192.168.1.2")
rob.set_tcp((0, 0, 0, 0, 0, 0))
rob.set_payload(2, (0, 0, 0.1))
sleep(0.2)  #leave some time to robot to process the setup commands

init_pose = [1.57, -1.57, -2.66, -0.6, -1.57, 0]
print("Resetting arm to start position. Please wait...")
rob.movej(init_pose, a, v)
print("Finished resetting arm to start position")


init_pose_robot = rob.get_pose(True).pos
print(init_pose_robot)

controller = OculusController()

prev_held_trigger = False
trigger_pressed = False
init_pos_controller = {0,0,0}

while(True):
    buttons = controller.get_buttons()
    triggerPressed = buttons['RTr']

    if(triggerPressed):
        if(not prev_held):
            print("New trigger")
            init_pos_controller = controller.get_cur_pos()[:3]
            init_pose_robot = rob.get_pose(True).pos.array_ref
            print("initial position set to : " + str(init_pos_controller))
            print("Initial robot pos set to: " + str(init_pose_robot))
        
        print()
        curr_pos_controller = controller.get_cur_pos()[:3]
        delta_controller = curr_pos_controller - init_pos_controller
        delta_controller[2] *= -1
        print("Delta is: " + str(delta_controller))
        delta_controller[1], delta_controller[2] = delta_controller[2], delta_controller[1] # y is z

        goal_pos_robot = init_pose_robot + delta_controller

        curr_pos_robot = rob.get_pose().pos.array_ref
        orientation = rob.get_pose().orient.log.array_ref
        movement = getMovement(curr_pos_robot, goal_pos_robot, orientation, max_movement)
        
        print("Robot delta is: " + str(movement))
        rob.servojInvKin(movement, wait=False, t=move_time)
        sleep(timeout)

        # rob.translate((desired_translation.x, desired_translation.y, desired_translation.z), a, v, wait=True)
        # sleep(0.5)

    else:
        rob.stopl(0.1)

    prev_held = triggerPressed
    # sleep(0.5)