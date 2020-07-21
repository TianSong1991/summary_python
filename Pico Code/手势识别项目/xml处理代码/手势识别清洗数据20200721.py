#!/usr/bin/env python
# coding: utf-8

# ## xml与png一一对应-删除无用png

# In[1]:


import os
import shutil


# In[2]:


path1 = r'E:\Pico\手势识别\data'


# In[3]:


for file0 in os.listdir(path1):
    path1_1 = os.path.join(path1,file0)
    for file1 in os.listdir(path1_1):
        path1_2 = os.path.join(path1_1,file1)
        path2 = os.path.join(path1,file0+'_only',file1)
        if not os.path.exists(path2):
            os.makedirs(path2)
        for file2 in os.listdir(path1_2):
            (name1,extension1) = os.path.splitext(file2)
            if extension1 == '.xml':
                path1_3 = os.path.join(path1_2,file2)
                path1_4 = os.path.join(path1_2,name1+'.png')
                shutil.move(path1_3,path2)
                shutil.move(path1_4,path2)


# ## 将数据提取出xml并打成rar压缩包

# In[10]:


import os
import shutil
path1 = r'E:\Pico\手势识别\data'


# In[11]:


for file0 in os.listdir(path1):
    path1_1 = os.path.join(path1,file0)
    path2_0 = os.path.join(path1,file0+'_xmlresult')
    for file1 in os.listdir(path1_1):
        path1_2 = os.path.join(path1_1,file1)
        path2 = os.path.join(path2_0,file1)
        if not os.path.exists(path2):
            os.makedirs(path2)
        for file2 in os.listdir(path1_2):
            (name1,extension1) = os.path.splitext(file2)
            if extension1 == '.xml':
                path1_3 = os.path.join(path1_2,file2)
                shutil.copy(path1_3,path2)
    shutil.make_archive(path2_0,'zip',path2_0)


# ## 检查标记点是否有标记为其他类别

# In[17]:


import os
import xml.etree.ElementTree as ET


xml_path0 = r'E:\Pico\手势识别\test_code'

keypoints = ['Wrist_L','Wrist','Wrist_R','Palm','Thumb_trap'
,'Thumb_meta','Thumb_prox','Thumb_dist','Thumb_tip','Index_prox'
,'Index_midd','Index_dist','Index_tip','Midd_prox','Midd_midd'
,'Midd_dist','Midd_tip','Ring_prox','Ring_midd','Ring_dist'
,'Ring_tip','Pinky_meta','Pinky_prox','Pinky_midd','Pinky_tip']

def check_number(obj,keypoints,path):
    num1 = len(keypoints)
    for i in range(num1):
        if obj.find(keypoints[i]):
            if int(obj.find(keypoints[i])[2].text) == 2:
                print(path,'Change Unknown 2 to 0 or 1')

def check_exist(obj,keypoints,path):
    num1 = len(keypoints)
    for i in range(num1):
        if not obj.find(keypoints[i]):
            print("Please Check keypoint not exist!!!",path)

def deal_xml(xml_path):
    for file00 in os.listdir(xml_path0):
        xml_path = os.path.join(xml_path0,file00)
        for file0 in os.listdir(xml_path):
            xml_path1 = os.path.join(xml_path,file0)
            for file1 in os.listdir(xml_path1):
                file_path = os.path.join(xml_path1,file1)
                (name1,extension1) = os.path.splitext(file1)
                if extension1 == '.xml':
                    tree=ET.parse(file_path)
                    root = tree.getroot()
                    for obj in root.iter('keyPoints'):
                        check_exist(obj,keypoints,file_path)
                        check_number(obj,keypoints,file_path)

if __name__ == '__main__':
    deal_xml(xml_path0) 
    print('done')


# ## 对手指关节点进行修改移动

# In[1]:


import os
import xml.etree.ElementTree as ET


# In[2]:


path1 = r'E:\Pico\手势识别\test_code\name5_only'#此路径为要被修改的xml
path2 = r'E:\Pico\手势识别\test_code\test'#此路径为提供标准的xml
keypoints = ['Index_prox','Midd_prox','Ring_prox','Pinky_prox']


# In[3]:


for file0 in os.listdir(path1):
    path1_1 = os.path.join(path1,file0)
    for file1 in os.listdir(path1_1):
        path1_2 = os.path.join(path1_1,file1)
        (name1,extension1) = os.path.splitext(file1)
        if extension1 == '.xml':
            path2_1 = os.path.join(path2,file0,file1)
            if os.path.exists(path2_1):
                tree0 = ET.parse(path1_2)
                root0 = tree0.getroot()
                tree1 = ET.parse(path2_1)
                root1 = tree1.getroot()
                for obj1 in root1.iter('keyPoints'):
                    num1 = len(keypoints)
                    for i in range(num1):
                        if obj1.find(keypoints[i]):
                            for obj0 in root0.iter('keyPoints'):
                                obj0.find(keypoints[i])[0].text = obj1.find(keypoints[i])[0].text
                                obj0.find(keypoints[i])[1].text = obj1.find(keypoints[i])[1].text  
                                tree=ET.ElementTree(root0)
                                tree.write(path1_2)
                





