#!/usr/bin/env python

import rospy
import rosnode
import roslaunch
from geometry_msgs.msg import Twist
from std_msgs.msg import String, Float64, UInt8
from std_srvs.srv import Empty
from std_srvs.srv import EmptyResponse


# @param timeout_ms Timeout for publishing in the topic (Warning: Precision of 10 miliseconds)
class Monitor_IsAlive():
    def __init__(self, topic, msg_type, timeout_ms):
        self.enabled = True
        self.running = False
        self.topic = topic

        if(timeout_ms < 10):
            rospy.logwarn("Monitor: Timeout value too small. Timer precision is 10 milliseconds")
            self.enabled = False
        else:
            if not ('/' + self.topic) in [item for i in rospy.get_published_topics() for item in i]:
                rospy.logerr("Monitor: Unable to subscribe to topic %s", self.topic)
                self.enabled = False
                return
            else:
                self.subs = rospy.Subscriber(topic, msg_type, self.TopicCallback)
                self.timer = rospy.Timer(rospy.Duration(0.01), self.TimerCallback, False)
                self.timeoutValue = int(timeout_ms / 10)


    def AttachCallback(self, timeoutCallback):
        self.actionCallback = timeoutCallback

    def Start(self):
        if self.enabled and callable(self.actionCallback):
            self.timeoutCounter = 0
            self.running = True

    # def Stop(self):
    #     self.timer.shutdown()

    def TopicCallback(self, data):
        self.timeoutCounter = 0     #reset timeout counter

    def TimerCallback(self, *args):
        if not self.enabled:
            self.running = False

        if(self.running):
            #Do additional operations if needed
            self.timeoutCounter += 1
            if(self.timeoutCounter >= self.timeoutValue):
                self.actionCallback()   # Execute action
                self.running = False