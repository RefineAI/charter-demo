import os
import sys

CAFFE_ROOT = "/home/icarus/installs/caffe"
sys.path.append(os.path.join(CAFFE_ROOT, 'python'))

import logging
import cv2
import caffe
import numpy
import cPickle
import time
import glob

IMAGENET_MEAN_FILE = os.path.join(CAFFE_ROOT, 'python/caffe/imagenet/ilsvrc_2012_mean.npy')
IMAGENET_BET_FILE = os.path.join(CAFFE_ROOT, 'data/ilsvrc12/imagenet.bet.pickle')


def find_model_files(path):
    try:
        model_file = glob.glob(os.path.join(path, "*deploy*.prototxt"))[0]
        print glob.glob(os.path.join(path, "*deploy*.prototxt"))
        pretrained_model_file = glob.glob(os.path.join(path, "*.caffemodel"))[0]
        return model_file, pretrained_model_file
    except:
        return None, None


class ImageRecognizer(object):
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = os.path.join(CAFFE_ROOT, "models/19_layers")

        model_file, pretrained_model_file = find_model_files(model_path)

        print model_file, pretrained_model_file

        self.net = caffe.Classifier(
            model_file, pretrained_model_file,
            image_dims=(256, 256), raw_scale=255,
            mean=numpy.load(IMAGENET_MEAN_FILE).mean(1).mean(1), channel_swap=(2, 1, 0)
        )

        self.labels = numpy.array(map(str.strip, open("synsets.txt").readlines()))

        self.bet = cPickle.load(open(IMAGENET_BET_FILE))
        self.bet['infogain'] -= numpy.array(self.bet['preferences']) * 0.1

        caffe.set_mode_gpu()

        self.net.forward()

    def classify_image(self, image):
        try:
            starttime = time.time()
            scores = self.net.predict([image], oversample=True).flatten()
            endtime = time.time()

            indices = (-scores).argsort()[:5]

            predictions = self.labels[indices]

            meta = [
                (p, '%.5f' % scores[i])
                for i, p in zip(indices, predictions)
            ]

            expected_infogain = numpy.dot(self.bet['probmat'], scores[self.bet['idmapping']])
            expected_infogain *= self.bet['infogain']

            infogain_sort = expected_infogain.argsort()[::-1]
            bet_result = [(self.bet['words'][v], '%.5f' % expected_infogain[v])
                          for v in infogain_sort[:20]]
            return meta

        except Exception as err:
            print 'Classification error: %s', err
            return (False, 'Something went wrong when classifying the image. Maybe try another one?')


def segment(im):
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = numpy.ones((3, 3), numpy.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.cv.CV_DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    # Finding unknown region
    sure_fg = numpy.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    ret, markers = cv2.findContours(sure_fg, cv2.cv.CV_RETR_EXTERNAL, cv2.cv.CV_CHAIN_APPROX_SIMPLE)

    markers = markers + 1

    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0

    markers = cv2.watershed(gray, markers)

    im[markers == -1] = [255, 0, 0]

    return gray


recognizer = ImageRecognizer()

cap = cv2.VideoCapture("/home/icarus/projects/charter-demo/tests/bond.mp4")

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        # f =segment(frame)
        # h,w = frame.shape[:2]
        # resized = cv2.pyrDown(frame, dstsize = (w/2, h/2))
        result = recognizer.classify_image(frame)
        print result
        cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()