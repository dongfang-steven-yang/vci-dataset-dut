# -*- coding: utf-8 -*-
"""
Created on Dec 26 2018
@author: Dongfang Yang
@email: yang.3455@osu.edu

These modules are used for pedestrian detection in drone video processing

"""
import cv2
import sys
import os
import numpy as np

def generate_background(file_name, dir_relative_source, dir_relative_backgrounds, roi, method='GSOC'):
    '''

    '''
    path_relative_background = dir_relative_backgrounds + file_name[11:][:-4] + '_background_' + method + '.png'
    existed_background = os.path.isfile(path_relative_background)
    if existed_background:
        frame_background = cv2.imread(path_relative_background)
        print('Background of '+file_name+' already exists, now loaded ...')
    else:
        if method == 'GSOC':
            bg_subtractor = cv2.bgsegm.createBackgroundSubtractorGSOC()
        elif method == 'MOG2':
            bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=200, detectShadows=False)  # default history=500
        else:
            print('Undefined background subtraction method!')

        # open video
        video = cv2.VideoCapture(dir_relative_source + file_name)
        width = int(video.get(3))
        height = int(video.get(4))
        fps = video.get(5)
        frame_total = video.get(cv2.CAP_PROP_FRAME_COUNT)

        # Exit if video not opened.
        if not video.isOpened():
            print
            "Could not open video"
            sys.exit()

        frame_index = 0
        # load new frame
        while True:
            # Read a new frame
            ok, frame = video.read()
            if not ok:
                break
            frame_index = frame_index + 1
            print('Generating background of '+file_name+', frames processed: '+str(frame_index)+'/'+str(frame_total)+' ...\r')

            # cropping frame
            frame = frame[roi[1]:(roi[1]+roi[3]), roi[0]:(roi[0]+roi[2])]
            frame_fgmask = bg_subtractor.apply(frame)
            frame_background = bg_subtractor.getBackgroundImage()

        cv2.imwrite(path_relative_background, frame_background)

    return frame_background