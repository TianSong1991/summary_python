#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# File  : model.py
# Author: Shuhao YUan (袁书豪)
# Data  : 18-4-27
# Email : 294663908@qq.com


from __future__ import division, print_function, absolute_import

# import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
import random
import json
import re



negative_root_dirs="/data/aaron/huaxun/phone/positive/0504_righthand_cam_right_down/1sic"





def negative_check_json():

    print("start read data")

    files1 = os.listdir(negative_root_dirs)


    for file3 in files1:

        (name1,extension1) = os.path.splitext(file3)
        if extension1 == '.json':
            json_file_path = os.path.join(negative_root_dirs,file3)
            h_file = open(json_file_path, 'r')
            landmark_json_string = h_file.read()
            h_file.close()
            try:
                landmark_json = json.JSONDecoder().decode(landmark_json_string)
            except:
                continue

            max_face_index=-1
            max_width=0

            face_index=-1
            for face in landmark_json["faces"]:
                face_index += 1
                width=max(face["face_rectangle"]["height"],face["face_rectangle"]["width"])
                if width>max_width:
                    max_width=width
                    max_face_index=face_index

            if max_face_index==-1:
                continue

            landmark = landmark_json["faces"][max_face_index]['landmark']

            min_x=10000
            max_x=-10000
            min_y=10000
            max_y=-10000

            print(json_path)
            for k in landmark:
                
                max_x = max(landmark[k]['x'], max_x)
                #print(max_x)
                min_x = min(landmark[k]['x'], min_x)
                #print(min_x)

                max_y = max(landmark[k]['y'], max_y)
                #print(max_y)
                min_y = min(landmark[k]['y'], min_y)
                #print(min_y) 
                






if __name__ == '__main__':

    negative_check_json()
