#!/usr/bin/env python2

import rospy
import tf

if __name__ == '__main__':
    rospy.init_node('fixed_tf_broadcaster')
    br_1 = tf.TransformBroadcaster()
    br_2 = tf.TransformBroadcaster()
    rate = rospy.Rate(50.0)
    
    while not rospy.is_shutdown():
        br_1.sendTransform((0.0, 0.0, 0.098),
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(),
                         "base_link",
                         "base_footprint")
        br_2.sendTransform((0.0, 0.0, 0.502),
                         (0.0, 0.0, 0.0, 1.0),
                         rospy.Time.now(),
                         "base_lidar_link",
                         "base_link")
        rate.sleep()