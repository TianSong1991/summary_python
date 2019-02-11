#-*- coding: utf-8 -*-

import os
import cv2
import shutil
import numpy as np
import math
import json

#原始路径
data_root_path = 'I:\\Project_FDS\\original_data\\HX_data\\data1120\\picture\\part1'

listfiles1 = os.listdir(data_root_path)

#保存路径
data_save_path = 'I:\\result'


for file1 in listfiles1:
    path1 = os.path.join(data_root_path,file1)
    json_file_dir = path1
    image_dir = path1
    json_file_list=os.listdir(json_file_dir)

    #print(json_file_dir)

    num=int(len(json_file_list)/2)

    #initialize the data
    mouth_images=np.zeros((200,200,num),dtype=np.uint8)

    i=0

    for json_file_name in json_file_list:

        random_shift_data_x = 0.2 * np.random.random() - 0.1  # -0.1到0.1之间
        random_shift_data_y = 0.2 * np.random.random() - 0.1  # -0.1到0.1之间
        random_scale_data = 0.2 * np.random.random() + 1.4  # 1.4到1.6之间

        (name1,extension1) = os.path.splitext(json_file_name)

        

        if extension1 == '.json':
            json_file_path=os.path.join(json_file_dir,json_file_name)
            h_file = open(json_file_path, 'r')
            landmark_json_string = h_file.read()
            h_file.close()

            landmark_json = json.JSONDecoder().decode(landmark_json_string)
            if len(landmark_json["faces"]) == 0:
            	continue
            landmark=landmark_json["faces"][0]['landmark']
            x_pixel = np.zeros(106, dtype=np.int32)
            y_pixel = np.zeros(106, dtype=np.int32)
            j = 0
            for k in landmark:
                x_pixel[j] = landmark[k]['x']
                y_pixel[j] = landmark[k]['y']
                j = j + 1

            max_x = np.max(x_pixel)
            min_x = np.min(x_pixel)
            max_y = np.max(y_pixel)
            min_y = np.min(y_pixel)

            width_ = max_x - min_x
            height_ = max_y - min_y
            if width_ > height_:
                width = width_
            else:
                width = height_
            left_up_point_ = (min_x, min_y)  # 此点英文left_down_point
            right_down_point_ = (min_x + width, min_y + width)  # 此点英文right_up_point
            center_point = ((left_up_point_[0] + right_down_point_[0]) / 2,
                           (left_up_point_[1] + right_down_point_[1]) / 2)

            left_up_point=(int(round(center_point[0]-width)),
                           int(round(center_point[1]-width)))

            # if left_up_point[0] < 0 or left_up_point[0] >= 640:
            #     continue
            # if left_up_point[1] < 0 or left_up_point[1] >= 480:
            #     continue

            right_down_point=(int(round(center_point[0]+width)),
                              int(round(center_point[1]+width)))

            # if right_down_point[0] < 0 or right_down_point[0] >= 640:
            #     continue
            # if right_down_point[1] < 0 or right_down_point[1] >= 480:
            #     continue
            #
            # if right_down_point[1] < left_up_point[1]  or right_down_point[0] < left_up_point[0]:
            #     continue
            (image_name, extension) = os.path.splitext(json_file_name)
            image_path = os.path.join(image_dir, image_name)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            range = int(1.2 * width)
            if (left_up_point[0] < 0 or left_up_point[1] < 0 or right_down_point[0] > 640 - 1 or right_down_point[1] > 480 - 1):
                image = np.zeros((480 + range * 2, 640 + range * 2), dtype=np.uint8)
                image_origin = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                image[(range - 1):(480 + range - 1), (range - 1):(640 + range - 1)] = image_origin

                center_point_new = (center_point[0] + range, center_point[1] + range)
                left_up_point = (int(center_point_new[0] - int(width)),
                                 int(center_point_new[1] - int(width)))
                right_down_point = (int(center_point_new[0] + int(width)),
                                    int(center_point_new[1] + int(width)))
                print(width)



            # image=cv2.imread(image_path,cv2.IMREAD_GRAYSCALE)
            roi=image[left_up_point[1]:right_down_point[1],left_up_point[0]:right_down_point[0]]

            #print(json_file_name)
            roi=roi/np.max(roi) #normalize

            mouth_image=cv2.resize(roi,(200,200))
            #mouth_image=roi
            mouth_images[:,:,i]=np.uint8(mouth_image*255)

            mouth_rect_image_dir=os.path.join(data_save_path,'smoke_rect')
            if not os.path.exists(mouth_rect_image_dir):
                os.makedirs(mouth_rect_image_dir)

            mouth_rect_image_path=os.path.join(mouth_rect_image_dir,file1+image_name)
            cv2.imwrite(mouth_rect_image_path,mouth_images[:,:,i])

            #print(json_file_name)

            i = i + 1
