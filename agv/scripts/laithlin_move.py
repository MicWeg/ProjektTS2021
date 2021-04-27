#!/usr/bin/env python3

import rospy
import sys
import argparse
import numpy
import time

import geometry_msgs.msg as gm
from move_base_msgs.msg import MoveBaseActionFeedback, MoveBaseActionGoal, MoveBaseActionResult, MoveBaseFeedback, MoveBaseResult
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Pose, PoseStamped, PoseArray, Quaternion
from tf.transformations import quaternion_from_euler
from actionlib_msgs.msg import GoalStatusArray, GoalID
from scipy.spatial import distance
from std_srvs.srv import EmptyRequest, Empty

#wspolrzedne punkyow (x, y, obrot z)
mir1_position = [[18.2, 18.6, 6.6, 6.9],
                 [10.6, 14.6, 5.1, 10.7],
                 [-0.71, -1.0, 0.71, -0.15]]
                 # [0.71, 0.00, 0.70, 0.99]]
mir2_position = [[14.2, 12.7, 11.4, 11.0],
                 [10.2, 14.7, 2.76, 11.0],
                 [0.0, 1.0, 0.7, 11.0]]
                 # [1.06, 0.0, 5.0, 11.0]]

#obecne wspolrzedne brane z feedback
pos_m1 = [0.0, 0.0]
pos_m2 = [0.0, 0.0]

m1_m = PoseStamped()
m2_m = PoseStamped()

#flagi do grafow
mir_status = [-1, -1]

#flaga startowa jak rowna zero to startuje
# f1 = 0


f_mir1 = 0
f_mir2 = 0

done1 = False
done2 = False
started1 = False
started2 = False
send1 = False
send2 = False
state_flag = False

collision = False

pub = rospy.Publisher('/mir_state', String, queue_size=10)
cancel_pub = rospy.Publisher("/mir2/move_base/cancel", GoalID, queue_size=1)

mir1_pub = rospy.Publisher("mir/move_base_simple/goal", PoseStamped, queue_size=5)
mir2_pub = rospy.Publisher("mir2/move_base_simple/goal", PoseStamped, queue_size=5)

def mir1_feed(data):
    # global pos_m1_x, pos_m1_y
    global pos_m1, mir_status
    location = data.feedback.base_position.pose
    status = data.status.status
    print(1, status)
    pos_m1 = [float(location.position.x), float(location.position.y)]
    mir_status[0] = status

    global done1
    if(not done1):
        done1 = True


def mir2_feed(data):
    global pos_m2, mir_status, state_flag
    
    location = data.feedback.base_position.pose
    status = data.status.status
    print(2, status)
    pos_m2 = [float(location.position.x), float(location.position.y)]
    mir_status[1] = status

    global done2
    if (not done2):
        done2 = True


def mir1_move(p_x, p_y, o_z):


    p = PoseStamped()

    p.header.seq = 1
    p.header.stamp = rospy.Time.now()
    p.header.frame_id = "map"

    p.pose.position.x = p_x
    p.pose.position.y = p_y
    p.pose.position.z = 0.0

    p.pose.orientation.x = 0.0
    p.pose.orientation.y = 0.0
    p.pose.orientation.z = o_z
    p.pose.orientation.w = 1.0

    return p


def mir2_move(p_x, p_y, o_z):

    p = PoseStamped()

    p.header.seq = 1
    p.header.stamp = rospy.Time.now()
    p.header.frame_id = "map"

    p.pose.position.x = p_x
    p.pose.position.y = p_y
    p.pose.position.z = 0.0

    p.pose.orientation.x = 0.0
    p.pose.orientation.y = 0.0
    p.pose.orientation.z = o_z
    p.pose.orientation.w = 1.0

    return p




def timer_callback(event):
    global mir_status, mir2_pub, m1_m, m2_m, \
        send1, send2, collision, started1, started2, cancel_pub, state_flag


    if collision is True:
        cancel_msg = GoalID()
        cancel_pub.publish(cancel_msg)
        print("mir2 is waiting")

        rospy.sleep(7)
        started2 = True
        collision = False

    if (done1 is True) and (done2 is True):
        pub.publish(mir_status)

    if (started2):
        mir2_pub.publish(m2_m)
        print("m2 send")
        started2 = False
        state_flag = True

    if (started1):
        mir1_pub.publish(m1_m)
        print("m1 send")
        started1 = False




def start():
    global f_mir1, f_mir2

    global m1_m, m2_m
    m1_m = mir1_move(mir1_position[0][0], mir1_position[1][0], mir1_position[2][0])
    m2_m = mir2_move(mir2_position[0][0], mir2_position[1][0], mir2_position[2][0])

    f_mir1 = 1
    f_mir2 = 1


def mir1_reach(m_r):
    global m1_m, f_mir1, send1, started1
    false_failure = False


    stat = m_r.status_list[0]


    stat_go1 = stat.status

    if stat_go1 == 1:
        send1 = True

    if stat_go1 == 4:
        rospy.wait_for_service('/mir/move_base_node/clear_costmaps')
        try:
            clear_costmap = rospy.ServiceProxy(
                '/mir/move_base_node/clear_costmaps', Empty)
            clear_costmap_trigger = EmptyRequest()
            clear_costmap(clear_costmap_trigger)
            started1=True
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
            return 0

        print("WARNING: mir1 detected posiible failure")
        if (f_mir1 == 0):
            if (mir1_position[0][0] + 1 > pos_m1[0] and mir1_position[0][0] - 1 < pos_m1[0] ) and (
                    mir1_position[1][0] + 1 > pos_m1[1] and mir1_position[1][0] - 1 < pos_m1[1] ):
                print("mir1 goal reached")
                false_failure = True

            else:
                print("ERROR: mir1 goal not reached")

        elif (f_mir1 == 1):
            if (mir1_position[0][1] + 1 > pos_m1[0] and mir1_position[0][1] - 1 < pos_m1[0]) and (
                    mir1_position[1][1] + 1 > pos_m1[1] and mir1_position[1][1] - 1 < pos_m1[1]):
                print("mir1 goal reached")
                false_failure = True

            else:
                print("ERROR: mir1 goal not reached")

        if (f_mir1 == 0):
            if (mir1_position[0][2] + 1 > pos_m1[0] and mir1_position[0][2] - 1 < pos_m1[0]) and (
                    mir1_position[1][2] + 1 > pos_m1[1] and mir1_position[1][2] - 1 < pos_m1[1]):
                print("mir1 goal reached")
                false_failure = True

            else:
                print("ERROR: mir1 goal not reached")


    if (stat_go1 == 3) or (false_failure is True):
        print("SUCESS: mir1 goal reached, waiting for next step")
        if (f_mir1 == 1) and (send1 is True):
            m1_m = mir1_move(mir1_position[0][1], mir1_position[1][1], mir1_position[2][1])
            print("mir 1 krok 2")
            f_mir1 = 2
            send1 = False


        elif (f_mir1 == 2) and (send1 is True):
            m1_m = mir1_move(mir1_position[0][2], mir1_position[1][2], mir1_position[2][2])
            print("mir 1 krok 3")
            f_mir1 = 0
            send1 = False


        elif (f_mir1 == 0) and (send1 is True):
            m1_m = mir1_move(mir1_position[0][0], mir1_position[1][0], mir1_position[2][0])
            print("mir 1 krok 1")
            f_mir1 = 1
            send1 = False


        false_failure = False

def mir2_reach(m_r):
    global m2_m, f_mir2, send2, stat_go2,started2

    false_failure = False


    stat = m_r.status_list[0]

    stat_go2 = stat.status

    if stat_go2 == 1:
        send2 = True

    dist = mir_distance()
    check_collision(dist)

    if stat_go2 == 4:
        rospy.wait_for_service('/mir2/move_base_node/clear_costmaps')
        try:
            clear_costmap = rospy.ServiceProxy(
                '/mir2/move_base_node/clear_costmaps', Empty)
            clear_costmap_trigger = EmptyRequest()
            clear_costmap(clear_costmap_trigger)
            started2=True
        except rospy.ServiceException as e:
            print("Service call failed: %s" % e)
            return 0

        print("WARNING: mir2 detected posiible failure")
        if (f_mir2 == 0):
            if (mir2_position[0][0] + 1 > pos_m2[0] and mir2_position[0][0] - 1 < pos_m2[0] ) and (
                    mir2_position[1][0] + 1 > pos_m2[1] and mir2_position[1][0] - 1 < pos_m2[1] ):
                print("mir2 goal reached")
                false_failure = True

            else:
                print("ERROR: mir2 goal not reached")

        elif (f_mir2 == 1):
            if (mir2_position[0][1] + 1 > pos_m2[0] and mir2_position[0][1] - 1 < pos_m2[0]) and (
                    mir2_position[1][1] + 1 > pos_m2[1] and mir2_position[1][1] - 1 < pos_m2[1]):
                print("mir2 goal reached")
                false_failure = True

            else:
                print("ERROR: mir2 goal not reached")

        if (f_mir2 == 0):
            if (mir2_position[0][2] + 1 > pos_m2[0] and mir2_position[0][2] - 1 < pos_m2[0]) and (
                    mir2_position[1][2] + 1 > pos_m2[1] and mir2_position[1][2] - 1 < pos_m2[1]):
                print("mir2 goal reached")
                false_failure = True

            else:
                print("ERROR: mir2 goal not reached")

    if (stat_go2 == 3) or (false_failure is True):
        print("SUCESS: mir2 goal reached, waiting for next step")
        if (f_mir2 == 1) and (send2 is True):
            m2_m = mir2_move(mir2_position[0][1], mir2_position[1][1], mir2_position[2][1])
            print("mir 2 krok 2")
            f_mir2 = 2
            send2 = False


        elif (f_mir2 == 2) and (send2 is True):
            m2_m = mir2_move(mir2_position[0][2], mir2_position[1][2], mir2_position[2][2])
            print("mir 2 krok 3")
            f_mir2 = 0
            send2 = False


        elif (f_mir2 == 0) and (send2 is True):
            m2_m = mir2_move(mir2_position[0][0], mir2_position[1][0], mir2_position[2][0])
            print("mir 2 krok 1")
            f_mir2 = 1
            send2 = False


        false_failure = False

def make_it_move(x):
    global started2, started1
    st = x
    if (st):
        started1 = True
        started2 = True

        st = False

def check_collision(distance):
    global collision

    if distance < 1:
        print("WARNING: collision detected")
        collision = True


#obliczanie dystansu miedzy robotami

def mir_distance():
    global pos_m1, pos_m2
    dist = distance.euclidean(pos_m1, pos_m2)
    print(dist)
    return dist

def make_it_happen():
    global f_mir1, f_mir2
    rospy.init_node('kfp_mir_move')

    if (f_mir1 == 0) and (f_mir2 == 0):
        start()

    #pobieranie statusu robotow
    rospy.Subscriber("/mir_move_next", Bool, make_it_move)
    rospy.Subscriber("mir/move_base/status", GoalStatusArray, mir1_reach)
    rospy.Subscriber("mir2/move_base/status", GoalStatusArray, mir2_reach)

    rospy.Subscriber("mir/move_base/feedback", MoveBaseActionFeedback, mir1_feed)
    rospy.Subscriber("mir2/move_base/feedback", MoveBaseActionFeedback, mir2_feed)
    timer = rospy.Timer(rospy.Duration(0.5), timer_callback)

    rospy.spin()
    timer.shutdown()


if __name__ == '__main__':
    try:
        make_it_happen()
    except rospy.ROSInterruptException:
        pass









