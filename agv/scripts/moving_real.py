#!/usr/bin/env python3
import rospy
import rosbag
from geometry_msgs.msg import PoseStamped
from actionlib_msgs.msg import GoalStatusArray
from std_srvs.srv import EmptyRequest, Empty


pose_goal_mir1 = []
i_mir1 = 0
pose_goal_mir2 = []
i_mir2 = 0

def load_poses(pose_list,name):

    try:
        bag = rosbag.Bag(name)
        for topics, msg, time in bag.read_messages(topics=['pose']):
            pose_list.append(msg)
        bag.close()
        return True
    except Exception as e:
        print(f"Couldn't load data {e}")
        return False


def check_pose_mir1(cur_pose1):
    global i_mir1
    status1 = cur_pose1

    if status1.status_list:
        if status1.status_list[-1].status == 4:

            rospy.wait_for_service('/mir/move_base/clear_costmaps')
            try:
                clear_costmap = rospy.ServiceProxy(
                    '/mir/move_base/clear_costmaps', Empty)
                clear_costmap_trigger = EmptyRequest()
                clear_costmap(clear_costmap_trigger)
                pub_mir1.publish(pose_goal_mir1[i_mir1])
            except rospy.ServiceException as e:
                print("Service call failed: %s" % e)
                return 0

    if (len(pose_goal_mir1) > 0) and status1.status_list:
        if (status1.status_list[-1].status == 3):
            i_mir1 += 1
            if (i_mir1 >= len(pose_goal_mir1)):
                i_mir1 = 0
            # for p in range(2):
            pub_mir1.publish(pose_goal_mir1[i_mir1])
                # rospy.sleep(0.1)


def check_pose_mir2(cur_pose2):
    global i_mir2
    status2 = cur_pose2
    if status2.status_list:
        if status2.status_list[-1].status == 4:

            rospy.wait_for_service('/mir2/move_base/clear_costmaps')
            try:
                clear_costmap = rospy.ServiceProxy(
                    '/mir2/move_base/clear_costmaps', Empty)
                clear_costmap_trigger = EmptyRequest()
                clear_costmap(clear_costmap_trigger)
                pub_mir2.publish(pose_goal_mir2[i_mir2])
                
            except rospy.ServiceException as e:
                print("Service call failed: %s" % e)
                return 0

    if (len(pose_goal_mir2) > 0) and status2.status_list:
        if (status2.status_list[-1].status == 3):
            i_mir2 += 1
            
            if (i_mir2 >= len(pose_goal_mir2)):
                i_mir2 = 0      
            # for p in range(2):
            pub_mir2.publish(pose_goal_mir2[i_mir2])
            #     rospy.sleep(2)
            # rospy.sleep(10)


rospy.init_node('moveDemo', anonymous=True)

pub_mir1 = rospy.Publisher('/mir/move_base_simple/goal', PoseStamped, queue_size=5)
pub_mir2 = rospy.Publisher('/mir2/move_base_simple/goal', PoseStamped, queue_size=5)

load_poses(pose_goal_mir1, 'pose_mir1')
load_poses(pose_goal_mir2, 'pose_mir2')

for p in range(2):
    pub_mir1.publish(pose_goal_mir1[0])
    pub_mir2.publish(pose_goal_mir2[0])
    rospy.sleep(0.1)

rospy.Subscriber("mir/move_base/status", GoalStatusArray, check_pose_mir1)
rospy.Subscriber("mir2/move_base/status", GoalStatusArray, check_pose_mir2)

while not rospy.is_shutdown():
    rospy.spin()
