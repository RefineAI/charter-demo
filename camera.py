#!/home/icarus/anaconda2/bin/python
import cv2
import skvideo.io
from skvideo.io import VideoWriter
import time
from AngusDriver import getFrame

from yolo import get_bounded_image
import angus



class VideoCamera(object):
    def __init__(self, videoFile):
        print "Camera Initialized"
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        print "Video File: " + videoFile
        self.video = skvideo.io.VideoCapture(videoFile)
        #self.video = cv2.VideoCapture(videoFile)
        #self.video =  skvideo.io.VideoCapture("/home/icarus/projects/MultiThreadPython/yttest.mp4")
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

    def __del__(self):
        self.video.release()


    def get_frame(self, service):
        success, frame = self.video.read()
        i = 0
        while(success):
            #img = cv2.imencode(".jpg", frame)
            #cv2.imwrite("test.jpg", frame)
            success, frame = self.video.read()
            #image = get_bounded_image(net, "/home/icarus/projects/angus/GOPR1379.MP4")
            if(i % 10 == 0):
                print "Frame: " + str(i)
                frame = getFrame(service, frame)
            ret, jpeg = cv2.imencode('.jpg', frame)
            print "Returning frame"
            return jpeg.tobytes()

    def get_frame_proxy(self, test):
        conn = angus.connect("https://gate.angus.ai", )
        service = conn.services.get_service("scene_analysis", version=1)
        service.enable_session()

        return self.get_frame(service)

