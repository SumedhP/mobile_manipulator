from oculus_controller import OculusController
import urx
from math3d.vector import PositionVector
from time import sleep
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import threading

# ROS ------
rclpy.init()
node = Node("oculus_controller_node")
velocity_publisher = node.create_publisher(Twist, '/cmd_vel', 10)

# Converts right joystick values to velocities for the
# neobotix base
def convertRightJSValuesToBaseVelocities(rightjs_values):
    js_x, js_y = rightjs_values
    # Scale velocities by 0.2 to limit base speed
    js_x = js_x * 0.2
    js_y = js_y * 0.2
    # x and y axes between oculus controller and base are flipped
    # polarity is also flipped in the x direction
    base_vel_x = js_y
    base_vel_y = -1 * js_x
    return [base_vel_x, base_vel_y]

def sendBaseVelocities(velocities):
    vel = Twist()
    vel.linear.x = velocities[0]
    vel.linear.y = velocities[1]
    vel.linear.z = 0.0
    velocity_publisher.publish(vel)

def controlBase(oculus_controller):
    while(True):
        controller_buttons = oculus_controller.get_buttons()
        trigger_is_pressed = controller_buttons['RTr']
        if trigger_is_pressed:
            rightjs_values = controller_buttons['rightJS']
            base_velocities = convertRightJSValuesToBaseVelocities(rightjs_values)
            sendBaseVelocities(base_velocities)


# URX -----
a = 1
v = 0.2

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

base_control_thread = threading.Thread(
    target=controlBase, args=(controller,))
base_control_thread.start()

prev_held_trigger = False
trigger_pressed = False
init_pos_controller = {0,0,0}

while(True):
    buttons = controller.get_buttons()
    triggerPressed = buttons['RTr']

    if(triggerPressed):
        if(not prev_held):
            print("New trigger")
            init_pos_controller = controller.get_cur_pos()
            init_pose_robot = rob.get_pose(True).pos
            print("initial position set to : " + str(init_pos_controller))
            print("Initial robot pos set to: " + str(init_pose_robot))
        
        print()
        curr_pos_controller = controller.get_cur_pos()
        delta_controller = curr_pos_controller - init_pos_controller
        delta_controller[2] *= -1
        print("Delta is: " + str(delta_controller))

        goal_pos_robot = PositionVector()
        print("Resetting robot pose to: " + str(init_pose_robot))
        goal_pos_robot.x = init_pose_robot.x + delta_controller[0]
        goal_pos_robot.y = init_pose_robot.y + delta_controller[2] # y is z
        goal_pos_robot.z = init_pose_robot.z + delta_controller[1]

        curr_pos_robot = rob.get_pose().pos
        desired_translation = goal_pos_robot - curr_pos_robot
        print("Robot delta is: " + str(desired_translation))
        rob.translate((desired_translation.x, desired_translation.y, desired_translation.z), a, v, wait=True)
        # sleep(0.5)

    else:
        rob.translate((0,0,0), a, v)

    prev_held = triggerPressed
    # sleep(0.5)