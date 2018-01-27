#!/usr/bin/env python2
import rospy
from geometry_msgs.msg import Twist, Pose2D, PoseStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from tf_conversions import transformations

class pybot():
    def __init__(self, cmd_vel_topic="cmd_vel", odom_topic="odom", scan_topic="base_scan"):
        self._pose_2d = Pose2D() 
        self._pose_stamped = PoseStamped()
        self._laser_scan = LaserScan()

        self._publishers = {}
        self._publishers["cmd_vel"] = rospy.Publisher( cmd_vel_topic, Twist, queue_size=10)
        
        rospy.Subscriber( scan_topic, LaserScan, self.__cb_laser_scan)
        rospy.Subscriber( odom_topic, Odometry, self.__cb_odom)
                

    def set_speed(self, linear, angular):
        t = Twist
        t.linear.x = linear
        t.angular.z = angular
        self._publishers["cmd_vel"].pub(t)

    def get_pose_2d():
        return self._pose_2d

    def get_pose_stamped():
        return self._pose_stamped

    def get_laser_scan():
        return self._laser_scan

    def __cb_odom(self, msg):
        self._pose_stamped.header = msg.header
        self._pose_stamped.pose = msg.pose.pose
        self._pose_2d.x = msg.pose.pose.position.x
        self._pose_2d.y = msg.pose.pose.position.y
        self._pose_2d.theta = transformations.euler_from_quaternion([
                msg.pose.pose.orientation.x,
                msg.pose.pose.orientation.y,
                msg.pose.pose.orientation.z,
                msg.pose.pose.orientation.w
                ])[2]

    def __cb_laser_scan(self, msg):
        self.__laser_scan = msg

def main():
    rospy.init_node("pybot")
    robot = pybot()
    rospy.spin()

if __name__ == "__main__":
    main()
