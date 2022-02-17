#!/usr/bin/env python

import rospy
import rosnode
import roslaunch


class Action_KillNode():
    def __init__(self, nodesToKill):
        self.nodes = nodesToKill

    def Execute(self):
        killed = rosnode.kill_nodes(self.nodes)
        rospy.loginfo("Killed nodes %s", killed[0])


class Action_CallService():
    # @param service Service to call
    # @param srv_type The ROS service type
    def __init__(self, service, srv_type):
        self.srv = service
        self.type = srv_type

    def Execute(self):
        try:
            service = rospy.ServiceProxy(self.srv, self.type)
            response = service()
            rospy.loginfo(response.message)
        except rospy.ServiceException as e:
            rospy.logerr("WTD action: %s - Service call failed: %s" % [self.srv, e])

class Action_PublishTopic():
    # @param topics Topic on which to publish the message 
    # @param msg_to_public The message to publish
    # @param msg_type The ROS message type of the topic. 
    def __init__(self, topic, msg_to_public, msg_type, queue_size = 10):
        self.topic = topic
        self.msg = msg_to_public
        self.msg_type = msg_type
        self.q_size = queue_size

    def Execute(self):
        try:
            pub = rospy.Publisher(self.topic, self.msg_type, queue_size=self.q_size)
            pub.publish(self.msg)
        except rospy.ServiceException as e:
            rospy.logerr("WTD action: Unable to publish to topic %s" % self.topic)



## Not impleented. ROS launch API is not stable enough. Use respawn and respawn_delay tag in .launch file instead
# class Action_KillAndReset():
#     def __init__(self, package_names, node_names, resetOffset_ms):
#         self.nodes = node_names
#         self.packs = package_names
#         self.resetOffset = resetOffset_ms

#     def Execute(self):
#         self.killed = rosnode.kill_nodes(self.nodes)
#         rospy.loginfo("WTD: Killed nodes: %s - Failed: %s", self.killed[0], self.killed[1])
        
#         if(len(self.killed[0]) > 0):    # If any node was successfully killed, start timer to reset
#             self.timer = rospy.Timer(rospy.Duration(self.resetOffset/1000), self.TimerCallback, True)


#     def TimerCallback(self, *args):
#         # for n in self.killed[0]:
#         rospy.loginfo('Restarting node.')
