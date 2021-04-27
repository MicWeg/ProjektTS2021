#!/usr/bin/env python

from agv.srv import state_srv,state_srvResponse
from actionlib_msgs.msg import GoalStatusArray
import rospy

state = 0

def state_callback(data):
    global state
    state = data.status_list[-1].status

def handler(req):
    global state
    rospy.Subscriber("mir/move_base/status", GoalStatusArray,state_callback)
    return state_srvResponse(state)

def state_server():
    rospy.init_node('state_server')
    server = rospy.Service('state_srv', state_srv, handler)
    rospy.spin()

if __name__ == "__main__":
    state_server()