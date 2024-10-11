#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int32MultiArray

def head_positions_callback(message):
    if len(message.data) >= 3:
        pos_motor1 = message.data[0]
        pos_motor2 = message.data[1]
        pos_motor3 = message.data[2]
        
        rospy.loginfo("Moteur 1: {}".format(pos_motor1))
        rospy.loginfo("Moteur 2: {}".format(pos_motor2))
        rospy.loginfo("Moteur 3: {}".format(pos_motor3))
        
        rospy.sleep(0.2)
    else:
        rospy.logwarn("Erreur : données insuffisantes.")

def motor_subscriber():
    rospy.init_node('motor_subscriber', anonymous=True)
    rospy.Subscriber('motors_positions', Int32MultiArray, head_positions_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        motor_subscriber()
    except rospy.ROSInterruptException:
        pass

