# coding: utf-8
#Author:TianSong
#Date:20180730

import os
import pandas as pd
import json
root_path = 'H:\\CallPhone\\CallPhone_4Cam_30_5.3\\Cam1\\IR'
os.chdir(root_path)
all_files = os.listdir()


data = {}
for files in all_files:
    i = 0
    subfiles = os.listdir(os.path.join(root_path,files))
    for subfile in subfiles:
        contentfiles = os.listdir(os.path.join(root_path,files,subfile))
        for contentfile in contentfiles:
            (filename,extention) = os.path.splitext(contentfile)
            if extention == '.json':
                json_file = open((os.path.join(root_path,files,subfile,contentfile)),'r')
                json_file_1 = json_file.read()
                json_file.close()
                json_file_2 = json.JSONDecoder().decode(json_file_1)
                if len(json_file_2["faces"]) == 0:
                    i = i+1
    data[files] = i    
data