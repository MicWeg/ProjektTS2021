#!/usr/bin/env python

from agv.srv import state_srv,state_srvResponse
from std_msgs.msg import Int64
import rospy

state = 0

def state_callback(data):
    global state
    state = data.data

def handler(req):
    global state
    rospy.Subscriber('/RobotState', Int64,state_callback)
    return state_srvResponse(state)

def state_server():
    rospy.init_node('state_server')
    server = rospy.Service('state_srv', state_srv, handler)
    rospy.spin()

if __name__ == "__main__":
    state_server()