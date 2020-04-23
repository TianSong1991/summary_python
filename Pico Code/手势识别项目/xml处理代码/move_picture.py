# Data:20200106
# Author:Kevin
# Project:Hand_Guesture

import os
import shutil

#移动出的路径，单独建立一个空文件夹
path1 = r'F:\data_guesture\pulldata'

def make_path(path1):
    if not os.path.exists(path1):
        os.makedirs(path1)

#每次运行必须修改name
name = 'Thumbup'

path_left = os.path.join('F:\\data_guesture',name,'lEye')
path_right = os.path.join('F:\\data_guesture',name,'rEye')
make_path(path_left)
make_path(path_right)

assert(len(os.listdir(path_left)) == 0)
assert(len(os.listdir(path_right)) == 0)

for file1 in os.listdir(path1):
    if file1.split('_')[0] == 'l':
    	shutil.move(os.path.join(path1,file1),path_left)
    else:
    	shutil.move(os.path.join(path1,file1),path_right)