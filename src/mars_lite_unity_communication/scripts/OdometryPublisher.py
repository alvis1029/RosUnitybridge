#!/usr/bin/env python2

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped, Twist, TransformStamped
import message_filters

# TF
import tf_conversions
import tf2_ros

class Force2CmdNode(object):
    def __init__(self):   
        self.pub_odom = rospy.Publisher('/odometry', Odometry, queue_size=1)
        self.sub_pose = message_filters.Subscriber('/wheel_odom', PoseStamped)
        self.sub_vel = message_filters.Subscriber('/wheel_vel', Twist)
        ts = message_filters.ApproximateTimeSynchronizer([self.sub_pose, self.sub_vel], 10, 0.1, allow_headerless=True)
        ts.registerCallback(self.callback)

        self.br = tf2_ros.TransformBroadcaster()
    
    def callback(self, pose_msg, twist_msg):
        cmd_msg = Odometry()
        cmd_msg.header.frame_id = pose_msg.header.frame_id
        cmd_msg.header.stamp = pose_msg.header.stamp
        cmd_msg.child_frame_id = "base_footprint"
        cmd_msg.pose.pose = pose_msg.pose
        cmd_msg.twist.twist = twist_msg

        self.pub_odom.publish(cmd_msg)

        # TF broadcaster
        tf_msg = TransformStamped()
        tf_msg.header = pose_msg.header
        tf_msg.child_frame_id = "base_footprint"
        tf_msg.transform.translation = cmd_msg.pose.pose.position
        tf_msg.transform.rotation = cmd_msg.pose.pose.orientation
        
        self.br.sendTransform(tf_msg)

if __name__ == '__main__':
    rospy.init_node('force2cmd_node', anonymous=False)
    node = Force2CmdNode()
    rospy.spin()