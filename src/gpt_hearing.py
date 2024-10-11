#! /usr/bin/env python3

import rospy
import openai

from std_msgs.msg import String

rospy.init_node('gpt_hearing', anonymous=True)
publisher1=rospy.Publisher('gpt_response', String, queue_size=1)



def gpt_hearing_callback(message):

	message_recu = message.data
		
	rospy.loginfo("Texte reçu : {}".format(message_recu))		
	completion = openai.chat.completions.create(
		model="gpt-4o-mini",
		messages=[
		    {"role": "system", "content": "Tu es un assistant et tu es intégré dans un code en python."},
		    {"role": "system", "content": "Il faut que ta réponse soit reconnaissable par le système de synthèse vocale pico2wave (pas de listes, de titres formatés...etc que du texte)."},
		    {"role": "user","content": "{}".format(message_recu)}
		]
	)
		
	reponse = completion.choices[0].message.content
		
	print("Réponse : {}".format(reponse))
		
	clean_reponse = reponse.replace("'","")

	print(clean_reponse)
	
	publisher1.publish(clean_reponse)
	
def gpt_hearing():
	rospy.Subscriber('speech_recognition/final_result', String, gpt_hearing_callback)	
	rospy.spin()	
if __name__ == '__main__':
	try:
		gpt_hearing()
	except rospy.ROSInterruptException:
		pass 
