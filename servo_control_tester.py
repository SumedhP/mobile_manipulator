import urx
from time import sleep, time
import math

a = 1
v = 0.2

# init_pose = [0, -1.57, -2.66, -0.6, -1.57, 0]
init_pose = [3.14, 0, 0, 0, 0, 0]


rob = urx.Robot("192.168.1.2", use_rt=True)
rob.set_tcp((0, 0, 0, 0, 0, 0))
rob.set_payload(2, (0, 0, 0.1))
sleep(0.2)  #leave some time to robot to process the setup commands

pos = rob.getj()
print(pos)

rob.movej(init_pose, a, v)
sleep(0.5)

pos = rob.getj()
print(pos)

for i in range(5):
    print("\nSending new movement")

    init_pose[0] -= math.radians(10)
    init_pose[1] -= math.radians(10)

    print("new pose: " + str(init_pose))
    
    prevTime = time()
    rob.servoj(init_pose,acc=5,vel=5, t=0.5, wait=True)
    print("time taken is: " + str(time() - prevTime))
    
    data = rob.get_all_rt_data(wait=False)
    print(data)

    # sleep(0.2)
    pos = rob.getj()
    print("Robot pos: " + str(pos))
    









#     # rob.movej(init_pose, a, v, wait=False)
#     # rob.translate((0.2,0,0), a, v, 0.05, wait=True)
#     # data = rob.get_all_rt_data(wait=False)
#     # print(data)
#     sleep(0.1)


# rob.movej((pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]+0.3), a, v)

