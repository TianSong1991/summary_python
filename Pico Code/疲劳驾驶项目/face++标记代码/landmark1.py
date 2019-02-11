import requests
import json
import cv2
import os

API_KEY = "uUs5WSPSfBO3stvPkUjzw_3kNFXhvG3S"
API_SECRET = "NURLsE_uqZ5-Q8s-jz8by8Rrk5EXHbg1"

base_path="I:\\test"
ir_dict_list=os.listdir(base_path)




def main():
    for sub_dir in ir_dict_list:
        dir_path=base_path+"\\"+sub_dir+"\\"

        if not os.path.isdir(dir_path):
            continue
        image_name_list=os.listdir(dir_path)
        for image_name in image_name_list:
            (filename, extension) = os.path.splitext(image_name)
            if extension=='.txt':
                continue
            if extension=='.json':
                continue
            if extension=='.points':
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
    data = {"api_key":API_KEY, "api_secret": API_SECRET, "return_landmark": "2","return_attributes":"headpose"}

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
                #print(json.dumps(req_dict, sort_keys=True, indent=2))
                for face in req_dict["faces"]:
                    for (k,v) in face["landmark"].items():
                        center=(v['x'],v['y'])
                        cv2.circle(image,center,1,(0,0,255),1)

                    pt1=(face["face_rectangle"]["left"],face["face_rectangle"]["top"])
                    pt2=(face["face_rectangle"]["left"]+face["face_rectangle"]["width"],face["face_rectangle"]["top"]+face["face_rectangle"]["height"])
                    cv2.rectangle(image,pt1,pt2,(255,0,0),1)
                #cv2.imshow("landmark", image)
                #cv2.waitKey(100)
                return req_con
            elif 'IMAGE_ERROR_UNSUPPORTED_FORMAT: image_file'== req_dict["error_message"]:
                print(req_dict)
                return
            else:
                #cv2.waitKey(100)
                print(req_dict)


if __name__=='__main__':
    for i in range(5):
        main()
        print("Done{0}".format(str(i)))