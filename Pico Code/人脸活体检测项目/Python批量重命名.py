# -*- coding:utf-8 -*-
# Author:Kevin Song
# Date:20181122
#将avi格式视频批量重命名为mp4格式
import os

depth_path = 'F:\\data1122\\depth\\2018_11_22'
count = 1
for file1 in os.listdir(depth_path):
    os.rename(os.path.join(depth_path,file1),os.path.join(depth_path,'name'+str(count)+'.mp4'))
    count = count + 1