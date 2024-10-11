#! /usr/bin/env python3

import rospy
import openai
import json

from std_msgs.msg import String
from std_msgs.msg import Int32MultiArray

rospy.init_node('gpt_hearing_moving', anonymous=True)

ratePublisher=rospy.Rate(1)

publisher1=rospy.Publisher('motors_commands', Int32MultiArray, queue_size=1)
publisher2=rospy.Publisher('video_commands', String, queue_size=1)
publisher3=rospy.Publisher('gpt_response', String, queue_size=1)

msg_posture = Int32MultiArray()
msg_video = String()

base_posture = [0,30,0,30,0,30,0,30]
happy_posture = [400,50,0,50,0,50,0,50]
sad_posture = [-100,50,0,50,30,50,0,50]
anger_posture = [[0,50,0,40,0,50,-350,50],[0,50,0,40,0,50,350,50]]	
surprise_posture = [0,50,-30,20,0,50,0,50]


happy_video = "/home/lutin/facepal/src/facepal_pkg/src/videos/happy.mp4"
sad_video = "/home/lutin/facepal/src/facepal_pkg/src/videos/sad.mp4"
anger_video = "/home/lutin/facepal/src/facepal_pkg/src/videos/anger.mp4"
surprise_video = "/home/lutin/facepal/src/facepal_pkg/src/videos/surprise.mp4"

rospy.sleep(1)

initialisation = []
initialisation.append({"role": "system", "content": "Tu es un assistant et tu es intégré dans un code en python."})
initialisation.append({"role": "system", "content": "Tu intéragis avec l'utilisateur comme si tu étais un camarade de classe qui peut être content, triste, énervé et surpris en fonction du contexte. pas d'émojis dans tes réponses ou de symboles comme */$/#..etc, que du texte."}),

function_descriptions = [
	{
		"name": "move",
		"description": "execute une commande en fonction d'un nombre donné par l'utilisateur. si le user bouge vers le bas change le signe du nombre en négatif. s'il veut bouger vers le haut change le signe en positif.",
		"parameters": {
			"type": "object",
			"properties": {
				"angle": {
					"type": "integer",
					"description":"c'est un angle en degrés",
				},
			},
		},
		"required": ["angle"],
		"additionalProperties": False,
	},
	{
		"name": "posture_expression",
		"description": "une commande pour exprimer une posture+une expression faciale. si le user te donne une bonne nouvelle, alors la valeur du paramètre est 1, si c'est une nouvelle triste alors c'est 2, si c'est une nouvelle qui énerve alors c'est 3, si c'est une surprise ou quelque chose d'inhabituel alors c'est 4",
		"parameters": {
			"type": "object",
			"properties": {
				"behaviour": {
					"type": "integer",
					"enum": [1,2,3,4],
					"description":"nombre entre 1 et 4",
				},
			},
		},
		"required": ["behaviour"],
		"additionalProperties": False,
	},
]

def posture_expression(behaviour):
	
	if behaviour==0:
		msg_posture.data = base_posture
		publisher1.publish(msg_posture)
		
	if behaviour==1:
		msg_video.data = happy_video
		publisher2.publish(msg_video)
		rospy.sleep(2)
		
		msg_posture.data = happy_posture
		publisher1.publish(msg_posture)
		return "happy"
		
	elif behaviour==2:
		msg_video.data = sad_video
		publisher2.publish(msg_video)
		rospy.sleep(2)
		
		msg_posture.data = sad_posture
		publisher1.publish(msg_posture)
		return "sad"
		
	elif behaviour==3:
		msg_video.data = anger_video
		publisher2.publish(msg_video)
		
		msg_posture.data = anger_posture[0]
		publisher1.publish(msg_posture)
		rospy.sleep(3)
		
		msg_posture.data = anger_posture[1]
		publisher1.publish(msg_posture)
		return "angry"
						
	elif behaviour==4:
		msg_video.data = surprise_video
		publisher2.publish(msg_video)
		
		msg_posture.data = surprise_posture
		publisher1.publish(msg_posture)
		return "surprised"
		
		
def move(angle):
	array_movement = [angle,50,0,0,0,0,0,0]
	msg_posture.data = array_movement
	
	print("MOVE")
	rospy.loginfo("Publishing : {}".format(msg_posture.data))
	publisher1.publish(msg_posture)
	
	
def gpt_hearing_moving_callback(message):
		result = String()
		prompt = message.data
		
		initialisation.append({"role": "user","content": prompt})
		
		first_completion = openai.chat.completions.create(
			model="gpt-4o-mini",
			messages=initialisation,
		)
				
		first_output = first_completion.choices[0].message
		result = first_output.content
		clean_result = result.replace("'","")
		
		print(result)
		publisher3.publish(clean_result)
		
		initialisation.append({"role": "assistant", "content": first_output.content})
		
		second_completion = openai.chat.completions.create(
				model="gpt-4o-mini",
				messages=initialisation,
				functions=function_descriptions,
				function_call="auto"
		)
		
		second_output = second_completion.choices[0].message
		print(second_output)
		
		if second_output.function_call:
			choosen_function = eval(second_output.function_call.name)
			params = json.loads(second_output.function_call.arguments)
			mood = choosen_function(**params)
			rospy.sleep(5)
			mood = posture_expression(0)
			
		print("Je vous écoute... Parlez...")

def gpt_hearing_moving():
	rospy.Subscriber('speech_recognition/final_result', String, gpt_hearing_moving_callback)
	rospy.spin()

if __name__ == '__main__':
	try:
		print("Je vous écoute... Parlez...")
		gpt_hearing_moving()
	except rospy.ROSInterruptException:
		pass

