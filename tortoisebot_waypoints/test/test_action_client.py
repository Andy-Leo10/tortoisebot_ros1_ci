#! /usr/bin/env python3

import rospy
import actionlib
from geometry_msgs.msg import Point
from tortoisebot_waypoints.msg import WaypointActionAction, WaypointActionGoal
import rosunit
import unittest
import rostest
PKG = 'tortoisebot_waypoints'
NAME = 'test_action_client'

class WaypointClient:
    def __init__(self):
        # Initialize the ROS node
        rospy.init_node('waypoint_client')
        # Create an action client
        self.client = actionlib.SimpleActionClient('tortoisebot_as', WaypointActionAction)
        # Wait for the action server to start
        self.client.wait_for_server()
        
        # results
        self.success_pos = False
        self.success_yaw = False

    def get_result_pos(self): return self.success_pos
    
    def get_result_yaw(self): return self.success_yaw
    
    def clean_results(self):
        self.success_pos = False
        self.success_yaw = False

    def send_goal(self, x, y, z):
        self.clean_results()
        # Create a goal object
        goal = WaypointActionGoal()
        goal.position = Point(x, y, z)  # Set your target waypoint here

        # Define a feedback callback
        def feedback_cb(feedback):
            rospy.loginfo('Feedback: %s' % feedback)
        # Send the goal to the action server
        self.client.send_goal(goal, feedback_cb=feedback_cb)

        # Wait for the server to finish performing the action
        self.client.wait_for_result()

        # Get the result of the action
        result = self.client.get_result()
        self.success_pos = result.success_pos
        self.success_yaw = result.success_yaw
        # Log the result
        # rospy.loginfo("Result Pos: %s" % ("Success" if self.success_pos else "Failure"))
        # rospy.loginfo("Result Yaw: %s" % ("Success" if self.success_yaw else "Failure"))

class TestWaypointClient1(unittest.TestCase):
    def setUp(self):
        self.waypoint_client = WaypointClient()

    def test_send_goal(self):
        self.waypoint_client.send_goal(0.0, 0.5, 0.0)
        rospy.loginfo("Result Pos: %s" % ("Success" if self.waypoint_client.get_result_pos() else "Failure"))
        rospy.loginfo("Result Yaw: %s" % ("Success" if self.waypoint_client.get_result_yaw() else "Failure"))
        self.assertEqual(self.waypoint_client.success_pos, True)
        self.assertEqual(self.waypoint_client.success_yaw, True)

class TestWaypointClient2(unittest.TestCase):
    def setUp(self):
        self.waypoint_client = WaypointClient()

    def test_send_goal(self):
        self.waypoint_client.send_goal(-0.5, 0.0, 0.0)
        rospy.loginfo("Result Pos: %s" % ("Success" if self.waypoint_client.get_result_pos() else "Failure"))
        rospy.loginfo("Result Yaw: %s" % ("Success" if self.waypoint_client.get_result_yaw() else "Failure"))
        self.assertEqual(self.waypoint_client.get_result_pos(), True)
        self.assertEqual(self.waypoint_client.get_result_yaw(), True)

if __name__ == '__main__':
    rostest.rosrun(PKG, NAME, 'test_action_client')
    '''
    this function expects the name of a Python module that contains the test cases
    not the name of a specific test case or test class
    You should pass the name of your test file (without the .py extension) as the 3rd argument 
    '''
