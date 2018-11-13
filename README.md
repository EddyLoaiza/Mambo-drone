# Mambo-drone
ROS python driver for parrot mambo drone 

This is the code that is explained in the report:

#!/usr/bin/env python3.5
import rospy
from std_msgs.msg import String, Empty
from geometry_msgs.msg import Twist
from pyparrot.Minidrone import Mambo
import sys, signal

#The address of our mambo drone according to he address shown
mamboAddr = "E0:14:A3:A5:3D:FD"#mambo1
#mamboAddr ="E0:14:AD:97:3D:FD"#mambo2
#mamboAddr = "D0:3A:3B:17:E6:36" #mambo3

mambo = Mambo(mamboAddr, use_wifi=False)
in_the_air = False 
hold_connection = True
wait = 0

def takeoff(self): 
    global in_the_air 
    if in_the_air == False:
        print("Taking off!")
        mambo.safe_takeoff(3)
        in_the_air = True 
    pass

def land(self):
    global in_the_air
    global rospy
    if in_the_air == True:
        in_the_air = False
        print("Trying to land")
        mambo.safe_land(2)
        mambo.smart_sleep(1)
        print("Almost there") 
        rospy.signal_shutdown("mambo landed")
        print("Landed")#to know it's being run up to here
    pass

def movement(data):
    global in_the_air
    global wait
    global mambo, hold_connection

    if in_the_air == True: 
        hold_connection = False
        wait=wait+1 
        if wait == 10: # when the counter gets to 0 then this condition is met and executed
            mambo.fly_direct(roll=(int(data.linear.y * 100)*(-1)), pitch=int(data.linear.x * 100), yaw=(int(data.angular.z * 100)*(-1)), vertical_movement=int(data.linear.z * 100), duration=0.01)
            wait = 0 
pass

def shutdown_hook():
    global in_the_air

    if in_the_air == True:
        print("exit_controlled: landing mambo")
        in_the_air = False
        mambo.safe_land(3)
        mambo.smart_sleep(2)
    print ('rospy is going down')
pass

def mambo_functions(): #the subscribing node
    global landed
    global rospy

    rospy.init_node('mambo_01') #initiate the code
    rospy.Subscriber("/mambo_01/takeoff", Empty, takeoff) 
    rospy.Subscriber("/mambo_01/land", Empty, land)
    rospy.Subscriber("/mambo_01/cmd_vel", Twist, movement)
    rospy.on_shutdown(shutdown_hook) 
    rospy.spin() 


if __name__ == '__main__':
    print(sys.version) 

    if True:
        print("trying to connect")
        success = mambo.connect(num_retries=20) 
        print("connected: %s" % success)
        if (success):
            print("wait! 4s")
            mambo.smart_sleep(2)
            mambo.ask_for_state_update()
            mambo.smart_sleep(2)
            print("Mambo 1 ready!")
            mambo_functions()
            print ('main: ros disconnect')
            mambo.disconnect()
            sys.exit(0)
