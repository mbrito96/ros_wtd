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
