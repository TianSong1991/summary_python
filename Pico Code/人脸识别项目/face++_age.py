# coding: utf-8
#Author:Sevn&Kevin
#Date:201809021

import requests
import json
import cv2
import os
import shutil
import time


API_KEY = "******"
API_SECRET = "*******"


base_path="F:\\face_recognization\\error"

move_path = "F:\\test"

notmove_path = "F:\\movepath"

if not os.path.exists(notmove_path):
	os.mkdir(notmove_path)

photo_lists1=os.listdir(base_path)


def main():
    for sub_dir in photo_lists1:
        dir_path=base_path+"\\"+sub_dir+"\\"
        if not os.path.isdir(dir_path):
            continue
        image_name_list=os.listdir(dir_path)
        for image_name in image_name_list:
            (filename, extension) = os.path.splitext(image_name)
            if extension=='.json':
                continue
            if extension=='.error':
                os.remove(dir_path + image_name)
                continue
            image_path = dir_path + image_name
            if os.path.exists(image_path+'.json'):
                continue
            print(image_path)
            result=detect(image_path)
            if result is None:
                txt_name = image_path + ".error"
                fh = open(txt_name, 'w')
                fh.write(image_path)
                fh.close()
                continue
            txt_name=image_path+".json"
            fh = open(txt_name, 'w')
            fh.write(result)
            fh.close()



def detect(image_path):
    data={}
    data['api_key']=API_KEY
    data['api_secret']=API_SECRET
    data = {"api_key":API_KEY, "api_secret": API_SECRET, "return_attributes":"age"}
    http_url ="https://api-cn.faceplusplus.com/facepp/v3/detect"
    files = {"image_file": open(image_path, "rb")}
    while True:
        try:
            response = requests.post(http_url, data=data, files=files)
            req_con = response.content.decode('utf-8')
        except Exception:
            print("something is wrong")
        else:
            req_dict = json.JSONDecoder().decode(req_con)
            if "error_message" not in req_dict.keys():
                image = cv2.imread(image_path)
                return req_con
            elif 'IMAGE_ERROR_UNSUPPORTED_FORMAT: image_file'== req_dict["error_message"]:
                print(req_dict)
                return
            else:
                print(req_dict)

def move_files():
	for file1 in os.listdir(base_path):
		path1 = os.path.join(base_path,file1)
		for file2 in os.listdir(path1):
			(name2,extension2) = os.path.splitext(file2)
			path2 = os.path.join(path1,file2)
			if extension2 == '.json':
				h_file=open(path2,'r')
				age_json_string=h_file.read()
				h_file.close()
				age_json=json.JSONDecoder().decode(age_json_string)
				if len(age_json['faces']) != 0:
					age_json=age_json['faces'][0]['attributes']['age']['value']
					path3=os.path.join(move_path,str(age_json))
					path4=os.path.join(path1,name2)
					if not os.path.exists(path3):
						os.makedirs(path3)
					shutil.copy(path4,path3) 
				else:
					path4=os.path.join(path1,name2)
					shutil.copy(path4,notmove_path)


if __name__=='__main__':
    main()
    print("Json is Done!")
    move_files()
