#!/usr/bin/env python3
#
"""Camera image classification demo code.

Runs continuous image classification on camera frames and prints detected object
classes.

Example:
image_classification_camera.py --num_frames 10
"""
import argparse
import contextlib
import servo
import time
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

    with PiCamera(sensor_mode=4, framerate=30, resolution=(1640, 1232)) as camera, \
         CameraPreview(camera, enabled=args.preview), \
         CameraInference(object_detection.model()) as inference:
        annotator = Annotator(camera, dimensions=(320, 240))
        scale_x = 320 / 1640
        scale_y = 240 / 1232    
        
        def transform(bounding_box):
            x, y, width, height = bounding_box
            return (scale_x * x, scale_y * y, scale_x * (x + width),
                    scale_y * (y + height))        
        
        
        
        for result in inference.run(args.num_frames):
            objs = object_detection.get_objects(result, threshold=0.3, offset=(0, 0))
#            objs = object_detection.get_classes(result)
            print (objs)
#
            annotator.clear()
            for obj in objs:
                print (obj.bounding_box[0])
                x0, y0, width, height = obj.bounding_box
                x = float((x0 + width/2) - 1640/2) #x range is -820 to 820
                y = float(1232/2 - (y0 + height/2)) #y range is -616 to 616
                print (obj.kind)
                print (obj.score)
                if obj.kind == 1 and obj.score > 0.5:
                    servo.triwalk(x/41) #820/20
#                    servo.rotate(x/18.222) #820/45
                    print('xval: %f', x/41)
                     
#                if obj.kind == 1 and obj.score > 0.5 and -100 <= x <= 100:
                    
#                annotator.bounding_box(transform(obj.bounding_box), fill=0)
#                
#            annotator.update()
#            if objs:
#                obj = objs[0]
#                x, y, width, height = obj.bounding_box


















#                print (obj.bounding_box)
#                camera.annotate_text = '%s' % objs[0]
#                print (camera.annotate_text)
#                if camera.annotate_text == 'mountain bike/all-terrain bike/off-roader':
#                    print ("bike!")

#servo.zero(0)
#time.sleep(1)
#servo.standup()   
#for x in range(4):
#    servo.triwalk(15)
#for x in range(4):
#    servo.rotate('r')    
#for x in range(4):
#    servo.rotate('l')   





if __name__ == '__main__':
    main()




