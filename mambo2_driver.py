#!/usr/bin/env python3.5
import rospy
from std_msgs.msg import String, Empty
from geometry_msgs.msg import Twist
from pyparrot.Minidrone import Mambo
import sys, signal

#The address of our mambo drone according to he address shown
mamboAddr = "E0:14:A3:A5:3D:FD"#mambo1
# remember to set True/False for the wifi depending on if we are using the wifi or the BLE to connect
mambo = Mambo(mamboAddr, use_wifi=False)
#Flags that will help us know the state of our drone
in_the_air = False # this is set to false because when we start the drone, it is waiting for a command on the ground
hold_connection = True
wait = 0

def takeoff(self): #Function to take off
    global in_the_air #we have to declare it once more because the function won't recognize it if it's out of it.
    if in_the_air == False:
        print("Taking off!")
        mambo.safe_takeoff(3)
        in_the_air = True # the state changes to true because it has taken off
    pass

def land(self):
    global in_the_air
    global rospy
    if in_the_air == True:
        in_the_air = False
        print("Trying to land")
        mambo.safe_land(2)
        mambo.smart_sleep(1)
        print("Almost there") #to know it's being run up to here
        rospy.signal_shutdown("mambo landed")
        print("Landed") # to know it's being run up to here
    pass

def movement(data):
    global in_the_air
    global wait
    global mambo, hold_connection

    if in_the_air == True: #this can only happen when the mambo is in the air
        hold_connection = False
        wait=wait+1 #counter. This counts in seconds starting at 0
        if wait == 10: # when the counter gets to 0 then this condition is met and executed
            mambo.fly_direct(roll=(int(data.linear.y * 100)*(-1)), pitch=int(data.linear.x * 100), yaw=(int(data.angular.z * 100)*(-1)), vertical_movement=int(data.linear.z * 100), duration=0.01)
            #the values from above, e.g data.linear.y, are taken from the "manual control code". It's multiplied by 100 to get values from 0 to 100 and it is turned to integer values
            wait = 0 #it's set to 0 again so the process can repeat
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
    rospy.Subscriber("/mambo_01/takeoff", Empty, takeoff) #to what topic, type of message and function to call
    rospy.Subscriber("/mambo_01/land", Empty, land)
    rospy.Subscriber("/mambo_01/cmd_vel", Twist, movement)
    rospy.on_shutdown(shutdown_hook) #Register handler to be called when rospy process begins shutdown. Request a callback
    rospy.spin() #It is mainly used to prevent your Python Main thread from exiting


if __name__ == '__main__':
    print(sys.version) #To know what python version is being used

    if True:
        print("trying to connect")
        success = mambo.connect(num_retries=20)    #connect(num_retries) connect to the Minidrone using BLE
                                                #You can specify a maximum number of re-tries. Returns true if the connection suceeded or False otherwise.
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
