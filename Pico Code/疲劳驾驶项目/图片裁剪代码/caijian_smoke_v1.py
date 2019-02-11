#-*- coding: utf-8 -*-

import os
import cv2
import shutil
import numpy as np
import math
import json

#原始路径
data_root_path = 'E:\\Project_FDS\\data_1030\\4mouth_smoke\\4mouth_smoke\\picture'

listfiles1 = os.listdir(data_root_path)

#保存路径
data_save_path = 'I:\\smoke_mouth111111'


for file1 in listfiles1:
    path1 = os.path.join(data_root_path,file1)
    json_file_dir = path1
    image_dir = path1
    json_file_list=os.listdir(json_file_dir)

    print(json_file_dir)

    num=int(len(json_file_list)/2)

    #initialize the data
    mouth_images=np.zeros((100,100,num),dtype=np.uint8)
    mouth_labels=np.zeros(num,dtype=np.int32)

    i=0

    j=0


    for json_file_name in json_file_list:

        random_shift_data_x = 0.2 * np.random.random() - 0.1  # -0.1到0.1之间
        random_shift_data_y = 0.2 * np.random.random() - 0.1  # -0.1到0.1之间
        random_scale_data = 0.2 * np.random.random() + 1.4  # 1.4到1.6之间


        (name1,extension1) = os.path.splitext(json_file_name)

        print(json_file_name)

        if extension1 == '.json':



            json_file_path=os.path.join(json_file_dir,json_file_name)
            h_file = open(json_file_path, 'r')
            landmark_json_string = h_file.read()
            h_file.close()

            landmark_json = json.JSONDecoder().decode(landmark_json_string)
            if len(landmark_json["faces"]) == 0:
            	continue
            landmark=landmark_json["faces"][0]['landmark']
            # print(landmark)

            faces = landmark_json["faces"]

            #print(j)
            j=j+1
            if 'headpose' not in faces[0]['attributes']:
                continue
            #print(faces)
            pitch_angle = faces[0]['attributes']['headpose']['pitch_angle']
            yaw_angle = faces[0]['attributes']['headpose']['yaw_angle']
            #print(pitch_angle)
            width=(landmark['mouth_right_corner']['x']-landmark['mouth_left_corner']['x'])*3.0#*1.6
            height=width

            # center_point=((landmark['mouth_right_corner']['x'] + landmark['mouth_left_corner']['x']) / 2.0 + random_shift_data_x*width,
            #               (landmark['mouth_right_corner']['y'] + landmark['mouth_left_corner']['y']) / 2.0+height*0.1 + random_shift_data_y*width)

            center_point=([(landmark['mouth_lower_lip_top']['x'] + landmark['mouth_upper_lip_bottom']['x']) / 2.0 ,
                          (landmark['mouth_lower_lip_top']['y'] + landmark['mouth_upper_lip_bottom']['y']) / 2.0])


            left_up_point=(round(center_point[0]-width/2.0),
                           round(center_point[1]-height/2.0))

            if left_up_point[0] < 0 or left_up_point[0] >= 640:
                continue
            if left_up_point[1] < 0 or left_up_point[1] >= 480:
                continue

            right_down_point=(round(center_point[0]+width/2.0),
                              round(center_point[1]+height/2.0))

            if right_down_point[0] < 0 or right_down_point[0] >= 640:
                continue
            if right_down_point[1] < 0 or right_down_point[1] >= 480:
                continue

            if right_down_point[1] < left_up_point[1]  or right_down_point[0] < left_up_point[0]:
                continue

            (image_name, extension) = os.path.splitext(json_file_name)
            image_path=os.path.join(image_dir,image_name)
            image=cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
            roi=image[left_up_point[1]:right_down_point[1],left_up_point[0]:right_down_point[0]]




            #print(json_file_name)
            roi=roi/np.max(roi) #normalize

            mouth_image=cv2.resize(roi,(100,100))
            #mouth_image=roi
            mouth_images[:,:,i]=np.uint8(mouth_image*255)


            #cv2.imshow("mouth",mouth_images[:,:,i])
            #print(i)


            #距离
            dx=landmark['mouth_right_corner']['x']-landmark['mouth_left_corner']['x']
            dy=landmark['mouth_right_corner']['y']-landmark['mouth_left_corner']['y']
            left_right_distance=math.sqrt(dx*dx+dy*dy)

            dx=landmark['mouth_upper_lip_bottom']['x']-landmark['mouth_lower_lip_top']['x']
            dy=landmark['mouth_upper_lip_bottom']['y']-landmark['mouth_lower_lip_top']['y']
            up_down_distance=math.sqrt(dx*dx+dy*dy)

            #比值
            v=up_down_distance/(left_right_distance+0.001)

            # if pitch_angle - 10.0 > 0:
            #     v = up_down_distance / (left_right_distance + 0.001) / (
            #             math.fabs(math.cos(pitch_angle * 3.1415926 / 180)) + 0.01) * (
            #             math.fabs(math.cos(yaw_angle * 3.1415926 / 180 * 0.65)))
            #
            #     v = v / math.fabs(math.cos(v * 2.0 + pitch_angle * 3.1415926 / 180)) + 0.01
            # else:
            #     v = up_down_distance / (left_right_distance + 0.001) / (
            #             math.fabs(math.cos((pitch_angle) * 3.1415926 / 180)) + 0.01) * (
            #             math.fabs(math.cos(yaw_angle * 3.1415926 / 180 * 0.65)))


            mouth_rect_image_dir=os.path.join(data_save_path,'smoke_rect')
            if not os.path.exists(mouth_rect_image_dir):
                os.makedirs(mouth_rect_image_dir)

            mouth_rect_image_path=os.path.join(mouth_rect_image_dir,file1+image_name)
            cv2.imwrite(mouth_rect_image_path,mouth_images[:,:,i])

            i = i + 1


