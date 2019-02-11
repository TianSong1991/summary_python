#-*- coding: utf-8 -*-
#Author:Mandy&Kevin
#Date:20180923

import requests
import json
import cv2
import os
import time
import shutil

base_path="F:\\face_recognization\\error"

ir_dict_list=os.listdir(base_path)

move_path = "F:\\test"

notmove_path = "F:\\movepath"

if not os.path.exists(notmove_path):
	os.mkdir(notmove_path)

def main():
    for sub_dir in ir_dict_list:
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
            time.sleep(3)
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
    subscription_key = "******"
    assert subscription_key
    face_api_url = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'content-type': "application/octet-stream"}
    params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age'
    }
    while True:
        try:
            with open(image_path, 'rb') as f:
                response = requests.post(face_api_url, params=params, headers=headers, data = f)
                req_con = response.content.decode('utf-8')
            print(response.json())
        except Exception:
            print("something is wrong")
        else:
            req_dict = json.JSONDecoder().decode(req_con)
            if "error_message" not in req_dict:
                image = cv2.imread(image_path)
                return req_con
            elif 'IMAGE_ERROR_UNSUPPORTED_FORMAT: image_file'== req_dict["error_message"]:
                print(req_dict)
                return
            else:
                print(req_dict)


def check_json():
    for file1 in ir_dict_list:
        path1 = os.path.join(base_path,file1)
        files2 = os.listdir(path1)
        for file2 in files2:
            (name1,extension1) = os.path.splitext(file2)
            if extension1 == '.json':
                json_path = os.path.join(path1,file2)
                json_file=open(json_path,'r')
                json_string=json_file.read()
                json_file.close()
                json_content=json.JSONDecoder().decode(json_string)
                if 'error' in json_content:
                    print(json_path)
                    os.remove(json_path)


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
                print(path2,":",age_json)
                if len(age_json) == 1:
                    age_json=int(age_json[0]['faceAttributes']['age'])
                    path3=os.path.join(move_path,str(age_json))
                    path4=os.path.join(path1,name2)
                    if not os.path.exists(path3):
                        os.makedirs(path3)
                    shutil.copy(path4,path3) 
                else:
                    path4=os.path.join(path1,name2)
                    shutil.copy(path4,notmove_path)

if __name__=='__main__':
    for i in range(3):
        main()
        print("Json is Done!"+str(i))
        check_json()
        print("Errr json delete done!"+str(i))
    move_files()
