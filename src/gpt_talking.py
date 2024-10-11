#!/usr/bin/env python3

import rospy
import os

from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient
from pydub import AudioSegment

def gpt_talking_callback(message):

	lecteur_audio = SoundClient()
	
	texte = message.data
	
	rospy.loginfo("Texte reçu : {}".format(texte))
	
	rospy.sleep(0.2)

	os.system("pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/reponse.wav '{}'".format(texte))

	rospy.sleep(0.5)
	
	audio = AudioSegment.from_wav("/home/lutin/facepal/src/facepal_pkg/src/videos/reponse.wav")
	audio_duration = len(audio) / 1000.0

	lecteur_audio.playWave("/home/lutin/facepal/src/facepal_pkg/src/videos/reponse.wav")
	
	rospy.sleep (audio_duration)
def gpt_talking():
	rospy.init_node('gpt_talking', anonymous=True)
	rospy.Subscriber('gpt_response', String, gpt_talking_callback)
	rospy.spin()
	
if __name__ == '__main__':
	try:
		gpt_talking()
	except rospy.ROSInterruptException:
		pass 
