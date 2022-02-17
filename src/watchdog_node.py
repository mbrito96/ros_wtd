#!/usr/bin/env python

from include.wtd_ros.actions import Action_CallService
import rospy
from wtd_ros import *
from geometry_msgs.msg import Twist
from std_msgs.msg import Float64, UInt8, Empty

wtd_arduino = Watchdog('arduino_wtd', True, 10.0)
wtd_mag = Watchdog('magnetometer_wtd', True, 10.0)


def watchdog_node():
    rospy.init_node('watchdog_node', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    # Arduino watchdog
    myWtd.AttachMonitor(Monitor_IsAlive('m1_yellow/pos', Float64, 500)) # Only need to detect one motor to know if Arduino has died
    myWtd.AttachAction(Action_KillNode(['rosserial_node']))

    myWtd.Start()

    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        watchdog_node()
    except rospy.ROSInterruptException:
        pass