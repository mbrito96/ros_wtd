#!/usr/bin/env python

import rospy
import rosnode
import roslaunch
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Float64, UInt8
from std_srvs.srv import Empty
from std_srvs.srv import EmptyResponse


class Watchdog:
    def __init__(self, name, respawn = False, respawn_offset_sec = 0.0):
        self.name = name
        self.monitors = []
        self.actions = []
        self.enabled = False
        self.triggered = False
        self.respawn = respawn
        self.respawn_offset = respawn_offset_sec

        self.srv_StartWtd = rospy.Service('/' + self.name + '/start', Empty, self.Start)
        self.srv_StopWtd = rospy.Service('/' + self.name + '/stop', Empty, self.Stop)

    # @param Monitor object to attatch to the watchdog. Monitors are appended to the list of monitors of the watchdog. The monitors are OR'd in order to trigger the actions.
    def AttachMonitor(self, monitorObj):
        self.monitors.append(monitorObj)
        for o in self.monitors:
            o.AttachCallback(self.WtdAction)

    def AttachAction(self, actionObj):
        self.actions.append(actionObj)

    def WtdAction(self):
        if not self.triggered:
            self.triggered = True
            for o in self.actions:
                o.Execute()
            # After performing action, check if need to respawn the watchdog
            if(self.respawn):
                self.triggered = False
                rospy.Timer(rospy.Duration(self.respawn_offset), self.Start, True)  # Oneshot timer

    def Start(self, arg = None):
        self.enabled = True
        for m in self.monitors:
            self.enabled &= m.enabled   ## Set to false if monitors failed
        if(self.enabled == True):
            for o in self.monitors:
                o.Start()
            rospy.loginfo(self.name + ' started.')
        else:
            rospy.loginfo(self.name + ' failed to start.')


        return EmptyResponse()

    def Stop(self, arg = None):
        self.enabled = False
        rospy.loginfo('Wtd stopped')
        return EmptyResponse()
