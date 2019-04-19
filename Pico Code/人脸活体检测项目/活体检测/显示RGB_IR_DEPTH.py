# -*- coding:utf-8 -*-
import os
import cv2
import sys
import matplotlib.pyplot as plt
import re
import shutil
from scipy.misc import bytescale
import numpy as np
from PIL import Image



def show_depth_img(Depth_path1):
    i = 1
    for file in os.listdir(Depth_path1):
        path1 = os.path.join(IR_path1,file)

        img16 = cv2.imread(path1,cv2.IMREAD_ANYDEPTH)

        #img8 = np.clip(img16,0,255).astype(np.uint8)

        img8 = cv2.convertScaleAbs(img16)

        cv2.imwrite(os.path.join(IR_path,str(i)+".png"),img8)        
        i = i + 1
        
        cv2.imshow('img8',img8)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def show_IR_img(IR_path1):
    def contrast_brightness_image(src1, a, g):
        h, w, ch = src1.shape

        src2 = np.zeros([h, w, ch], src1.dtype)
        dst = cv2.addWeighted(src1, a, src2, 1-a, g)
        return dst 
    i = 1
    for file in os.listdir(IR_path1):
        path1 = os.path.join(IR_path1,file)

        img16 = cv2.imread(path1,cv2.IMREAD_ANYDEPTH)

        img8 = img16.reshape(480,640,1)
        
        # cv2.imshow('img8',img8)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        img = contrast_brightness_image(img8, 20, 50)
        cv2.imwrite(os.path.join(IR_path,str(i)+".png"),img)        
        i = i + 1


#同时显示rgb、ir、depth三图进行查看
def show_IR_Depth_img(IR_path1,Depth_path1):
#########################IR#################################

    (name2,extension2) = os.path.split(IR_path1)
    (name3,extension3) = os.path.split(name2)
    (name4,extension4) = os.path.split(name3)
    irname = "ir:"+extension4+":"+extension2
    (name5,extension5) = os.path.split(Depth_path1)
    (name6,extension6) = os.path.split(name5)
    (name7,extension7) = os.path.split(name6)
    depthname = "depth:"+extension7+":"+extension5
    def contrast_brightness_image(src1, a, g):
        h, w, ch = src1.shape
        src2 = np.zeros([h, w, ch], src1.dtype)
        dst = cv2.addWeighted(src1, a, src2, 1-a, g)
        #cv2.imshow("con-bri-demo", dst)
        return dst 

    irimg16 = cv2.imread(IR_path1,cv2.IMREAD_ANYDEPTH)
    irimg8 = irimg16.reshape(480,640,1)
    img = contrast_brightness_image(irimg8, 20, 50)
    cv2.imshow(irname,img)
############################Depth##################################
    depthimg16 = cv2.imread(Depth_path1,cv2.IMREAD_ANYDEPTH)
    #img8 = np.clip(img16,0,255).astype(np.uint8)
    depthimg8 = cv2.convertScaleAbs(depthimg16)
    cv2.imshow(depthname,depthimg8)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



def main():
    path1 = 'I:\\Project_FaceDetection\\Data_Tengxun\\02_Tidy_data\\stronglight\\data0215\\part3'

    for file1 in os.listdir(path1):
        rgb_path = os.path.join(path1,file1,'rgb')
        ir_path = os.path.join(path1,file1,'ir')
        depth_path = os.path.join(path1,file1,'depth')
        for file2 in os.listdir(rgb_path):
            (name1,extension1) = os.path.splitext(file2)
            rgb_image = os.path.join(rgb_path,file2)
            ir_image = os.path.join(ir_path,name1+".png")
            depth_image = os.path.join(depth_path,name1+".png")
            rgb8 = cv2.imread(rgb_image)
            cv2.imshow(file2,rgb8)
            show_IR_Depth_img(ir_image,depth_image)
    #         show_IR_img(ir_image)
    #         show_depth_img(depth_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
