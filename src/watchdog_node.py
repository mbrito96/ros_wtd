#!/usr/bin/env python

import rospy
from wtd_ros import *
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64, UInt8, Empty

myWtd = Watchdog('myWtd', True, 10.0)


def watchdog_node():
    rospy.init_node('watchdog_node', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    # Arduino watchdog
    myWtd.AttachMonitor(Monitor_IsAlive('m1_yellow/pos', Float64, 500))
    # myWtd.AttachMonitor(Monitor_IsAlive('m2_orange/pos', Float64, 500))
    # myWtd.AttachMonitor(Monitor_IsAlive('m3_blue/pos', Float64, 500))
    myWtd.AttachAction(Action_KillNode(['rosserial_node']))
    myWtd.Start()

    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        watchdog_node()
    except rospy.ROSInterruptException:
        pass