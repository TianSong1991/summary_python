# -*- coding:utf-8 -*-
#Author:Kevin Song
#Date:20181208
import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join


classes = ["phone", "smoke"]

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def tran_txt_saveimagepath():
    path1 = '/media/pico/886835D26835C02C/colleague/done_landmark_save/03_Train_data/big/200_200'
    #save_path = '/home/pico/darknet/data/downdata/'
    image_path_file = open('/home/pico/darknet/data/downdata/fds_picturepath.txt', 'w')
    listfiles1 = os.listdir(path1)
    for file1 in listfiles1:
        path1_1 = os.path.join(path1,file1)
        listfiles2 = os.listdir(path1_1)
        for file2 in listfiles2:
            path1_2 = os.path.join(path1_1,file2)
            listfiles3 = os.listdir(path1_2)
            for file3 in listfiles3:
                path1_3 = os.path.join(path1_2,file3)
                listfiles4 = os.listdir(path1_3)
                for file4 in listfiles4:
                    (name1,extension1) = os.path.splitext(file4)
                    xml_path = os.path.join(path1_3,file4)
                    if extension1 == '.xml':
                        #print(xml_path)
                        txt_path = os.path.join(save_path,file1,file2,file3)
                        if not os.path.exists(txt_path):
                            os.makedirs(txt_path)                    
                        in_file = open(xml_path)
                        tree=ET.parse(in_file)
                        root = tree.getroot()
                        size = root.find('size')
                        w = int(size.find('width').text)
                        h = int(size.find('height').text)
                        for obj in root.iter('object'):
                            difficult = obj.find('difficult').text
                            cls = obj.find('name').text
                            if cls not in classes or int(difficult) == 1:
                                continue
                            cls_id = classes.index(cls)
                            xmlbox = obj.find('bndbox')
                            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
                            bb = convert((w,h), b)
                            #out_file = open(os.path.join(save_path,file1,file2,file3,name1+'.txt'), 'w')
                            out_file = open(os.path.join(path1_3,name1+'.txt'), 'w')
                            out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
                            out_file.close()
                    else :
                        image_path_file.write(xml_path+'\n')
    image_path_file.close()

if __name__ == '__main__':
    tran_txt_saveimagepath()
