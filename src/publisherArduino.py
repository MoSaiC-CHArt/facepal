#!/usr/bin/env python3

import rospy

from std_msgs.msg import Int32
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import String

nodeName='angle'
topicName='motors_commands'
videoTopicName='video_commands'

rospy.init_node(nodeName, anonymous=True)

publisher1=rospy.Publisher(topicName, Int32MultiArray, queue_size=1)
publisher2=rospy.Publisher(videoTopicName, String, queue_size=1)

ratePublisher=rospy.Rate(1)


while not rospy.is_shutdown():
	try:
		
		print("--MOTOR1--", end='\n')
		array1_input = input("ANGLE (degrés) [ESPACE] VITESSE (tours/min) : ")
		print("--MOTOR2--", end='\n')
		array2_input = input("ANGLE (degrés) [ESPACE] VITESSE (tours/min) : ")
		print("--MOTOR3--", end='\n')
		array3_input = input("ANGLE (degrés) [ESPACE] VITESSE (tours/min): ")
		print("--MOTOR4--", end='\n')
		array4_input = input("ANGLE (degrés) [ESPACE] VITESSE (tours/min) : ")
		print("--VIDEO--", end='\n')
		video_input = input("Path to video (~/path/to/video.avi) : ")
        
		array1 = [int(x) for x in array1_input.split()]
		array2 = [int(x) for x in array2_input.split()]
		array3 = [int(x) for x in array3_input.split()]
		array4 = [int(x) for x in array4_input.split()]
		
		multi_array = [array1, array2, array3, array4]
		
		msg = Int32MultiArray()
		
		for sublist in multi_array:
			msg.data.extend(sublist)
			
		video_msg = String()
		video_msg.data = video_input
		
		print(video_input)
		
		rospy.loginfo("Publishing : {}".format(msg.data))
		publisher1.publish(msg)
		
		rospy.loginfo("Publishing : {}".format(video_msg.data))
		publisher2.publish(video_msg)
			
		#input_msg = input("Position + vitesse ( entre 50 et 300 ) : ")
		#positions = [int(x) for x in input_msg.split()]
		#array_msg = Int32MultiArray(data=positions)
		#print(array_msg.data)
			
	except ValueError:
		print("Valeur erronnée.")	
	ratePublisher.sleep()
