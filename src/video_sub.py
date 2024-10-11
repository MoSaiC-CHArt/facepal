#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import cv2
import os

class VideoPlayer:
    def __init__(self):
        self.default_video = "/home/lutin/facepal/src/facepal_pkg/src/videos/neutral.mp4"
        self.current_video = self.default_video
        self.video_window_name = 'cute face'
        self.new_video_requested = False
        
        rospy.init_node('video_subscriber', anonymous=True)
        rospy.Subscriber('video_commands', String, self.video_callback)
    
    def video_callback(self, msg):
        new_video_path = msg.data
        print(msg.data)
        
        if new_video_path != self.current_video:
            self.current_video = new_video_path
            self.new_video_requested = True
            rospy.loginfo("Changement de vidéo : {}".format(self.current_video))
    
    def play_video(self, video_path):
        if not os.path.isfile(video_path):
            rospy.logerr("Le fichier vidéo n'existe pas: {}".format(video_path))
            return
            
        vid = cv2.VideoCapture(video_path)
        
        if not vid.isOpened():
            rospy.logerr("Erreur lors de l'ouverture du fichier: {}".format(video_path))
            return
            
        cv2.namedWindow(self.video_window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(self.video_window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
	
        while vid.isOpened():
            ret, frame = vid.read()
            if not ret or self.new_video_requested:
                break
                
            frame_resized = cv2.resize(frame, (800,480))
                
            cv2.imshow(self.video_window_name, frame_resized)
            if cv2.waitKey(30) & 0xFF == ord('q'):
                rospy.signal_shutdown("User pressed 'q'")
                break
                        
        vid.release()
        
        if self.new_video_requested:
            self.new_video_requested = False
            
        if video_path != self.default_video:
            self.current_video = self.default_video
        
    def run(self):
        cv2.namedWindow(self.video_window_name, cv2.WINDOW_NORMAL)
        while not rospy.is_shutdown():
            rospy.loginfo("Vidéo en cours: {}".format(self.current_video))
            self.play_video(self.current_video)

if __name__ == '__main__':
    try:
        video_player = VideoPlayer()
        video_player.run()
    except rospy.ROSInterruptException:
        pass

