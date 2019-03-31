#!/usr/bin/env python3
"""Camera image classification demo code.

Runs continuous image classification on camera frames and prints detected object
classes.

Example:
image_classification_camera.py --num_frames 10
"""
import argparse
import contextlib
import servo
import LED
import time
from multiprocessing import Process
#from concurrent.futures import ThreadPoolExecutor
#import _thread
#from threading import Thread
from aiy.vision.inference import CameraInference
from aiy.vision.models import object_detection
from picamera import PiCamera
from aiy.vision.annotator import Annotator

def classes_info(classes):
    return ', '.join('%s (%.2f)' % pair for pair in classes)

@contextlib.contextmanager
def CameraPreview(camera, enabled):
    if enabled:
        camera.start_preview()
    try:
        yield
    finally:
        if enabled:
            camera.stop_preview()

def main():
    parser = argparse.ArgumentParser('Image classification camera inference example.')
    parser.add_argument('--num_frames', '-n', type=int, default=None,
        help='Sets the number of frames to run for, otherwise runs forever.')
    parser.add_argument('--num_objects', '-c', type=int, default=3,
        help='Sets the number of object interences to print.')
    parser.add_argument('--nopreview', dest='preview', action='store_false', default=True,
        help='Enable camera preview')
    args = parser.parse_args()
    
#    servo.standup()

    with PiCamera(sensor_mode=4, framerate=30, resolution=(1640, 1232)) as camera, \
         CameraPreview(camera, enabled=args.preview), \
         CameraInference(object_detection.model()) as inference:
#        annotator = Annotator(camera, dimensions=(320, 240))
#        scale_x = 320 / 1640
#        scale_y = 240 / 1232    
        
#        def transform(bounding_box):
#            x, y, width, height = bounding_box
#            return (scale_x * x, scale_y * y, scale_x * (x + width),
#                    scale_y * (y + height))        

        for result in inference.run(args.num_frames):
            objs = object_detection.get_objects(result, threshold=0.3, offset=(0, 0))
            print (objs)
#            annotator.clear()
#            for obj in objs:                                     
#                annotator.bounding_box(transform(obj.bounding_box), fill=0)
#            annotator.update()
            if objs:
                obj = objs[0]
                x, y, width, height = obj.bounding_box
                                
                print (obj.bounding_box[0])
                x0, y0, width, height = obj.bounding_box
                x = float((x0 + width/2) - 1640/2) #x range is -820 to 820
                y = float(1232/2 - (y0 + height/2)) #y range is -616 to 616
                print (obj.kind)
                print (obj.score)

#                pool = ThreadPoolExecutor(5)               
                if obj.kind == 1 and obj.score > 0.5: 
                    LED.color(0,0,255)
                    Process(target=servo.triwalk, args=(x/41,))
#                   future = pool.submit(servo.triwalk, (x/41))
                    
#                    _thread.start_new_thread(servo.triwalk,(x/41,)) #820/20
#                    _thread.start_new_thread(LED.color,(0,0,255,))
#                    _thread.start_new_thread(servo.rotate,(x/18.222,)) #820/45

#                    servo.triwalk(x/41) #820/20
#                    print('xval: %f', x/41)
#                    servo.rotate(x/18.222) #820/45
#                    print('xval: %f', x/18.222)
                    if -50<x<50:
                        LED.color(0,255,0) #Green = I'm aiming at you
                else:
                    LED.color(255,0,0) #Red = where are you?






#                print (obj.bounding_box)
#                camera.annotate_text = '%s' % objs[0]
#                print (camera.annotate_text)
#                if camera.annotate_text == 'mountain bike/all-terrain bike/off-roader':
#                    print ("bike!")

if __name__ == '__main__':
    main()



