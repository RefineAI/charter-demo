import cv2

import numpy as np
import StringIO
import datetime
import pytz
from math import cos, sin
#from skvideo.io import VideoWriter

import angus

def getFrame(service, frame):
    #angus.con



    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, buff = cv2.imencode(".jpg", gray, [cv2.IMWRITE_JPEG_QUALITY, 80])
    buff = StringIO.StringIO(np.array(buff).tostring())
    t = datetime.datetime.now(pytz.utc)
    # print("Calling service")
    job = service.process({"image": buff,
                           "timestamp": t.isoformat()
                           })
    # print("Called service")
    res = job.result
    print str(res)
    if "error" in res:
        print("Bomb")
        print(res["error"])
    else:
        # This parses the entities data
        print("No Bomb")
        for key, val in res["entities"].iteritems():
            print("Iterating")
            # display only gaze vectors
            # retrieving eyes points
            eyel, eyer = val["face_eye"]
            eyel = tuple(eyel)
            eyer = tuple(eyer)

            # retrieving gaze vectors
            psi = 0
            g_yaw, g_pitch = val["gaze"]
            theta = - g_yaw
            phi = g_pitch

            # Computing projection on screen
            # and drawing vectors on current frame
            length = 150
            xvec = int(length * (sin(phi) * sin(psi) - cos(phi) * sin(theta) * cos(psi)))
            yvec = int(- length * (sin(phi) * cos(psi) - cos(phi) * sin(theta) * sin(psi)))
            cv2.line(frame, eyel, (eyel[0] + xvec, eyel[1] + yvec), (0, 140, 0), 3)

            xvec = int(length * (sin(phi) * sin(psi) - cos(phi) * sin(theta) * cos(psi)))
            yvec = int(- length * (sin(phi) * cos(psi) - cos(phi) * sin(theta) * sin(psi)))
            cv2.line(frame, eyer, (eyer[0] + xvec, eyer[1] + yvec), (0, 140, 0), 3)

        service.disable_session()
        return frame

if __name__ == '__main__':
    getFrame()











