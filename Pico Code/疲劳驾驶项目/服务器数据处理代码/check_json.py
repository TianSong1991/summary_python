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



data_root_dir="/data/aaron/huaxun/phone"


# 获取样本路径
positive_root_dir=os.path.join(data_root_dir,"positive")
negative_root_dir=os.path.join(data_root_dir,"negative")

positive_root_dirs=[positive_root_dir]
negative_root_dirs=[negative_root_dir, "/data/aaron/negative"]
# configure end #############################################################



positive_set=[]
negative_set=[]

# 递归
def append_bmp(dir,ispositive):
    file_list=os.listdir(dir)
    for file in file_list:
        file_path=os.path.join(dir,file)
        if os.path.isdir(file_path):
            append_bmp(file_path,ispositive)
        else:
            (file_name,file_ex)=os.path.splitext(file)
            if file_ex==".json":
                if ispositive:
                    positive_set.append(file_path)
                else:
                    negative_set.append(file_path)


for positive_root_dir in positive_root_dirs:
    append_bmp(positive_root_dir,True)
#append_bmp(positive_root_dir.replace("positive","false_negative"),True)
for negative_root_dir in negative_root_dirs:
    append_bmp(negative_root_dir,False)
#append_bmp(negative_root_dir.replace("negative","false_positive"),False)


# 样本数量
num_positive=len(positive_set)
num_negative=len(negative_set)

print("the number of positive samples is:",num_positive)
print("the number of negative samples is:",num_negative)



def positive_check_json():

    print("start read data")

    for i in range(num_positive):

        print(i)


        json_file_path=positive_set[i]

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
        for k in landmark:
            print(json_path)
            max_x = max(landmark[k]['x'], max_x)
            print(max_x)
            min_x = min(landmark[k]['x'], min_x)
            print(min_x)

            max_y = max(landmark[k]['y'], max_y)
            print(max_y)
            min_y = min(landmark[k]['y'], min_y)
            print(min_y)


def negative_check_json():

    print("start read data")

    for j in range(num_negative):

        print(j)


        json_file_path=negative_set[j]

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
        for k in landmark:
            print(json_path)
            max_x = max(landmark[k]['x'], max_x)
            print(max_x)
            min_x = min(landmark[k]['x'], min_x)
            print(min_x)

            max_y = max(landmark[k]['y'], max_y)
            print(max_y)
            min_y = min(landmark[k]['y'], min_y)
            print(min_y) 




if __name__ == '__main__':
    positive_check_json()
    negative_check_json()
