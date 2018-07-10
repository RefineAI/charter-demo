#!/home/icarus/anaconda2/bin/python
from flask import Flask
from flask import g
from flask_cors import CORS, cross_origin
from flask import request, Response, stream_with_context, render_template, redirect, url_for, send_file
from camera import VideoCamera
from subprocess import call
import cv2

# Make sure that caffe is on the python path:
caffe_root = '/home/icarus/installs/caffe/'
import sys
sys.path.insert(0, caffe_root + 'python')
import time
import caffe
import os
import yaml
import random
import json

app = Flask(__name__, template_folder='.', static_url_path = "", static_folder = "static")

net = None

def init():
    global net
    print "In Init function"
    model_filename = '/home/icarus/projects/charter-demo/models/yolo-deploy-prototxt'
    weight_filename = '/home/icarus/projects/charter-demo/models/yolo.caffemodel'
    #img_filename = '/home/icarus/projects/AgeGender/images/Male.jpeg'
    net = caffe.Net(model_filename, weight_filename, caffe.TEST)


@app.route('/frame' ,methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def processFrame():
    print "In Frame"
    res = "Some JSON"
    print "Sending response"
    resp = Response(response=res,
                    status=200,
                    mimetype="application/json")

    return resp


@app.route("/downloadUrl" ,methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def download():
    url = request.args.get("url")
    print "Generating random Int"
    videoId = random.randrange(1000,9999)
    print "generated random int" + str(videoId)
    fileName = "/home/icarus/projects/AgeGender/videos/" + str(videoId) + ".mp4"
    print "Dest File: " + fileName
    command = "youtube-dl -f 18 -o " + fileName +  "  " + url + " -c"
    print "Command to run: " + command
    call(command.split(), shell=False)
    #AnalyzeAndSaveVideo(nets, fileName)
    return "http://34.207.96.9:8000/stream?videoId=" + str(videoId) + ".mp4"


@app.route("/proxyStream" ,methods=['GET', 'POST' , 'OPTIONS'])
@cross_origin()
def proxyRequest():
    r = request.args.get("url", stream=True)
    return Response(r.iter_content(chunk_size=10 * 1024),
                    content_type=r.headers['Content-Type'])


def gen(camera):
    while True:
        frame = camera.get_frame_proxy()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/streamWithAnnotation' ,methods=['GET', 'POST' ,'OPTIONS'])
@cross_origin()
def video_feed():
    print "In Annotation Stream"
    #videoId = request.args.get("videoId")
    fileName = "/home/icarus/projects/charter-demo/tests/bond.mp4"
    #fileName="/home/icarus/projects/angus/GOPR1379.MP4"
    #fileName = "/home/icarus/projects/charter-demo/chase.mp4"
    return Response(gen(VideoCamera(fileName)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/stream" ,methods=['GET', 'POST' ,'OPTIONS'])
@cross_origin()
def stream():
    #videoId = request.args.get("videoId")
    fileName = "/home/icarus/projects/charter-demo/tests/bond.mp4"
    print "File to fetch: " + fileName
    g = file(fileName)  # or any generator
    return Response(g, direct_passthrough=True)


@app.route("/test" ,methods=['GET', 'POST' ,'OPTIONS'])
@cross_origin()
def processTest():
    companyId = request.args.get("companyId")
    participantId = request.args.get("participantId")
    campaignId = request.args.get("campaignId")
    return "Test processing: " + companyId + " " + participantId + " " + campaignId





@app.route('/')
@app.route('/index')
@cross_origin()
def default():
    return "Hello There!!!"


if __name__ == '__main__':
   init()
   app.run(host='0.0.0.0', port=7500, threaded=True, debug=True)
