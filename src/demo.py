#!/usr/bin/env python3

import rospy
import os

from std_msgs.msg import Int32
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import String
from sound_play.libsoundplay import SoundClient

nodeName='demo'
topicName='motors_commands'
videoTopicName='video_commands'

rospy.init_node(nodeName, anonymous=True)

publisher1=rospy.Publisher(topicName, Int32MultiArray, queue_size=1)
publisher2=rospy.Publisher(videoTopicName, String, queue_size=1)

ratePublisher=rospy.Rate(1)


while not rospy.is_shutdown():
	try:
		
		lecteur_audio = SoundClient()
		
		os.system("pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/bonjour.wav 'Bonsoir à tous, ceci est une démonstration'")
		
		rospy.sleep(0.5)
		
		os.system("pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/presentation.wav 'Pour commencer, je mexcuse car vous pouvez mentendre mais moi, je ne peux pas, car Massile na pas encore fini de linstaller.'")
		
		rospy.sleep(0.5)
		
		os.system(" pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/presentation2.wav 'Maintenant, je vais vous montrer mes degrés de liberté. Ensuite, les expressions faciales que je peux afficher à lécran.'")
		
		rospy.sleep(0.5)
		
		os.system("pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/rotation_gauche.wav 'Pour les rotations, je peux tourner dans ce sence.'")
		
		rospy.sleep(0.5)
		
		os.system("pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/rotation_droite.wav 'Et je peux tourner dans le sence inverce.'")
		
		rospy.sleep(0.5)
		
		os.system("pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/tete_haut.wav 'Ensuite, je peux bouger la tête vers le haut.'")
		
		rospy.sleep(0.5)
		
		os.system("pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/tete_bas.wav 'Et, enfin, je peux bouger la tête vers le bas'")
		
		rospy.sleep(0.5)
		
		os.system("pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/introduction_expressions.wav '`A présent, je vais vous montrer quelques expressions faciales. Je les afficherai sur lécran.'")
		
		rospy.sleep(0.5)
		
		os.system("pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/joie.wav 'Dabord, je suis heureuse.'")
		
		rospy.sleep(0.5)
		
		os.system("pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/surprise.wav 'Ensuite, je suis surprise.'")
		
		rospy.sleep(0.5)
		
		os.system("pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/triste.wav 'Puis, je suis triste.'")
		
		rospy.sleep(0.5)
		
		os.system("pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/colere.wav 'Pour finir, je suis en colère.'")
		
		rospy.sleep(0.5)
		
		os.system("pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/massyl.wav 'Pour le reste des mouvements, nous allons revenir dessus plus tard.'")
		
		rospy.sleep(0.5)
		
		os.system("pico2wave -l fr-FR -w /home/lutin/facepal/src/facepal_pkg/src/videos/massyl2.wav 'Revenons maintenant aux deux derniers mouvements. Pour ces deux là, je vais avoir besoin de ton aide, Massile.'")
		
		rospy.sleep(0.5)
		
		joie = "/home/lutin/facepal/src/facepal_pkg/src/videos/happy.mp4"
		colere = "/home/lutin/facepal/src/facepal_pkg/src/videos/anger.mp4"
		triste = "/home/lutin/facepal/src/facepal_pkg/src/videos/sad.mp4"
		surprise = "/home/lutin/facepal/src/facepal_pkg/src/videos/surprise.mp4"
		
		array_rotation1 = [0,0,0,0,0,0,-800,50]
		array_rotation2 = [0,0,0,0,0,0,800,50]
		
		array_haut = [400,50,0,0,0,0,0,0]
		array_bas = [-400,50,0,0,0,0,0,0]
		
		msg = Int32MultiArray()
		msg.data = array_rotation1
		
		video_msg = String()			
		
		lecteur_audio.playWave('/home/lutin/facepal/src/facepal_pkg/src/videos/bonjour.wav')
		
		
		rospy.sleep(4)
		
		#publisher1.publish(msg2)
		
		#rospy.sleep(2)
		
		lecteur_audio.playWave('/home/lutin/facepal/src/facepal_pkg/src/videos/presentation.wav')
		
		rospy.sleep(10)
		
		lecteur_audio.playWave('/home/lutin/facepal/src/facepal_pkg/src/videos/presentation2.wav')
		
		rospy.sleep(9)
		
		lecteur_audio.playWave('/home/lutin/facepal/src/facepal_pkg/src/videos/rotation_gauche.wav')
		
		rospy.sleep(3)
		
		publisher1.publish(msg)
		
		rospy.sleep(4)
		
		lecteur_audio.playWave('/home/lutin/facepal/src/facepal_pkg/src/videos/rotation_droite.wav')
		
		rospy.sleep(2)
		
		msg.data = array_rotation2
		publisher1.publish(msg)
		
		rospy.sleep(4)
		
		lecteur_audio.playWave('/home/lutin/facepal/src/facepal_pkg/src/videos/tete_haut.wav')
		
		rospy.sleep(2)
		
		msg.data = array_haut
		publisher1.publish(msg)
		
		rospy.sleep(2)
		
		lecteur_audio.playWave('/home/lutin/facepal/src/facepal_pkg/src/videos/tete_bas.wav')
		
		rospy.sleep(3)
		
		msg.data = array_bas
		publisher1.publish(msg)
		
		rospy.sleep(2)
		
		lecteur_audio.playWave('/home/lutin/facepal/src/facepal_pkg/src/videos/massyl.wav')
		
		rospy.sleep(4)
		
		lecteur_audio.playWave('/home/lutin/facepal/src/facepal_pkg/src/videos/introduction_expressions.wav')
		
		rospy.sleep(7)
		
		lecteur_audio.playWave('/home/lutin/facepal/src/facepal_pkg/src/videos/joie.wav')
		
		rospy.sleep(1)
		
		video_msg.data = joie
		publisher2.publish(video_msg)
		
		rospy.sleep(10)
		
		lecteur_audio.playWave('/home/lutin/facepal/src/facepal_pkg/src/videos/surprise.wav')
		
		rospy.sleep(1)
		
		video_msg.data = surprise
		publisher2.publish(video_msg)
		
		rospy.sleep(14)
		
		lecteur_audio.playWave('/home/lutin/facepal/src/facepal_pkg/src/videos/triste.wav')
		
		rospy.sleep(1)
		
		video_msg.data = triste
		publisher2.publish(video_msg)
		
		rospy.sleep(12)
		
		lecteur_audio.playWave('/home/lutin/facepal/src/facepal_pkg/src/videos/colere.wav')
		
		rospy.sleep(1)
		
		video_msg.data = colere
		publisher2.publish(video_msg)
		
		rospy.sleep(7)
		
		lecteur_audio.playWave('/home/lutin/facepal/src/facepal_pkg/src/videos/massyl2.wav')
		
		rospy.sleep(7)	
		rospy.signal_shutdown("Execution finished")
		
	except ValueError:
		print("Valeur erronnée.")	
	ratePublisher.sleep()
