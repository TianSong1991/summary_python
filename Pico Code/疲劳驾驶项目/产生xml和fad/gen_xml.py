#-*- coding: utf-8 -*-

import json
import os
import shutil
from xml.dom.minidom import Document
import re

doc=Document()


class xml_write():
    def __init__(self):
        self.count=0
        self.pattern=r"([0-9]+)\s+([0-9]+)"
        self.pattern2 = r"version"
        self.parts=[]
    def write(self,string):
        if re.search(self.pattern2,string):
            self.count=0
            self.parts=[]
            return

        result=re.search(self.pattern,string)
        if result is None:
            return

        part=doc.createElement("part")
        part.setAttribute("name","%02d"%(self.count))
        part.setAttribute("x", result.group(1))
        part.setAttribute("y", result.group(2))
        self.count += 1

        self.parts.append(part)

        return part

    def get_parts(self):
        return self.parts



def create_image_element(image_dict):
    if len(image_dict["faces"]) == 0:
        return

    image=doc.createElement("image")


    for face in image_dict["faces"]:
        fw = xml_write()
        fw.write("version: 1\nn_points:  68\n{\n")
        landmark = face["landmark"]

        # 轮廓
        point = landmark["contour_left2"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["contour_left4"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["contour_left6"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["contour_left8"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["contour_left10"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["contour_left12"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["contour_left14"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        # point=landmark["contour_left16"]
        # fw.write("%d %d\n"%(point['x'],point['y']))

        point1 = landmark["contour_left16"]
        point2 = landmark["contour_left15"]
        fw.write("%d %d\n" % ((point1['x'] + point2['x']) / 2, (point1['y'] + point2['y']) / 2))

        point = landmark["contour_chin"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        # point=landmark["contour_right16"]
        # fw.write("%d %d\n"%(point['x'],point['y']))

        point1 = landmark["contour_right16"]
        point2 = landmark["contour_right15"]
        fw.write("%d %d\n" % ((point1['x'] + point2['x']) / 2, (point1['y'] + point2['y']) / 2))

        point = landmark["contour_right14"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["contour_right12"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["contour_right10"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["contour_right8"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["contour_right6"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["contour_right4"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["contour_right2"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        # 眼眉
        point = landmark["left_eyebrow_left_corner"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["left_eyebrow_upper_left_quarter"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["left_eyebrow_upper_middle"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["left_eyebrow_upper_right_quarter"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["left_eyebrow_upper_right_corner"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["right_eyebrow_upper_left_corner"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["right_eyebrow_upper_left_quarter"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["right_eyebrow_upper_middle"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["right_eyebrow_upper_right_quarter"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["right_eyebrow_right_corner"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        # 鼻子

        point = landmark["nose_bridge1"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["nose_bridge2"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["nose_bridge3"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["nose_tip"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["nose_left_contour4"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["nose_left_contour5"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["nose_middle_contour"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["nose_right_contour5"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["nose_right_contour4"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        # 眼睛
        point = landmark["left_eye_left_corner"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point1 = landmark["left_eye_upper_left_quarter"]
        point2 = landmark["left_eye_top"]
        fw.write(
            "%d %d\n" % ((point1['x'] * 2.0 / 3.0 + point2['x'] / 3.0), (point1['y'] * 2.0 / 3.0 + point2['y'] / 3.0)))

        point1 = landmark["left_eye_upper_right_quarter"]
        point2 = landmark["left_eye_top"]
        fw.write(
            "%d %d\n" % ((point1['x'] * 2.0 / 3.0 + point2['x'] / 3.0), (point1['y'] * 2.0 / 3.0 + point2['y'] / 3.0)))

        point = landmark["left_eye_right_corner"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point1 = landmark["left_eye_lower_right_quarter"]
        point2 = landmark["left_eye_bottom"]
        fw.write(
            "%d %d\n" % ((point1['x'] * 2.0 / 3.0 + point2['x'] / 3.0), (point1['y'] * 2.0 / 3.0 + point2['y'] / 3.0)))

        point1 = landmark["left_eye_lower_left_quarter"]
        point2 = landmark["left_eye_bottom"]
        fw.write(
            "%d %d\n" % ((point1['x'] * 2.0 / 3.0 + point2['x'] / 3.0), (point1['y'] * 2.0 / 3.0 + point2['y'] / 3.0)))

        point = landmark["right_eye_left_corner"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point1 = landmark["right_eye_upper_left_quarter"]
        point2 = landmark["right_eye_top"]
        fw.write(
            "%d %d\n" % ((point1['x'] * 2.0 / 3.0 + point2['x'] / 3.0), (point1['y'] * 2.0 / 3.0 + point2['y'] / 3.0)))

        point1 = landmark["right_eye_upper_right_quarter"]
        point2 = landmark["right_eye_top"]
        fw.write(
            "%d %d\n" % ((point1['x'] * 2.0 / 3.0 + point2['x'] / 3.0), (point1['y'] * 2.0 / 3.0 + point2['y'] / 3.0)))

        point = landmark["right_eye_right_corner"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point1 = landmark["right_eye_lower_right_quarter"]
        point2 = landmark["right_eye_bottom"]
        fw.write(
            "%d %d\n" % ((point1['x'] * 2.0 / 3.0 + point2['x'] / 3.0), (point1['y'] * 2.0 / 3.0 + point2['y'] / 3.0)))

        point1 = landmark["right_eye_lower_left_quarter"]
        point2 = landmark["right_eye_bottom"]
        fw.write(
            "%d %d\n" % ((point1['x'] * 2.0 / 3.0 + point2['x'] / 3.0), (point1['y'] * 2.0 / 3.0 + point2['y'] / 3.0)))

        # 嘴唇
        point = landmark["mouth_left_corner"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_upper_lip_left_contour2"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_upper_lip_left_contour1"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_upper_lip_top"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_upper_lip_right_contour1"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_upper_lip_right_contour2"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_right_corner"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_lower_lip_right_contour2"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_lower_lip_right_contour3"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_lower_lip_bottom"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_lower_lip_left_contour3"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_lower_lip_left_contour2"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        # point1 = landmark["mouth_upper_lip_left_contour2"]
        # point2 = landmark["mouth_lower_lip_left_contour2"]
        # fw.write("%d %d\n"%((point1['x']+point2['x'])/2,(point1['y']+point2['y'])/2))

        # point1 = landmark["mouth_upper_lip_left_contour3"]
        # point2 = landmark["mouth_upper_lip_left_contour4"]
        # fw.write("%d %d\n"%((point1['x']+point2['x'])/2,(point1['y']+point2['y'])/2))
        point = landmark["mouth_upper_lip_left_contour3"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_upper_lip_left_contour4"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_upper_lip_bottom"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_upper_lip_right_contour4"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_upper_lip_right_contour3"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        # point1 = landmark["mouth_upper_lip_right_contour3"]
        # point2 = landmark["mouth_upper_lip_right_contour4"]
        # fw.write("%d %d\n"%((point1['x']+point2['x'])/2,(point1['y']+point2['y'])/2))

        # point1 = landmark["mouth_upper_lip_right_contour2"]
        # point2 = landmark["mouth_lower_lip_right_contour2"]
        # fw.write("%d %d\n"%((point1['x']+point2['x'])/2,(point1['y']+point2['y'])/2))

        point = landmark["mouth_lower_lip_right_contour1"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        # point1 = landmark["mouth_lower_lip_right_contour2"]
        # point2 = landmark["mouth_lower_lip_right_contour3"]
        # fw.write("%d %d\n"%((point1['x']+point2['x'])/2,(point1['y']+point2['y'])/2))

        point = landmark["mouth_lower_lip_top"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        point = landmark["mouth_lower_lip_left_contour1"]
        fw.write("%d %d\n" % (point['x'], point['y']))

        # point1 = landmark["mouth_lower_lip_left_contour2"]
        # point2 = landmark["mouth_lower_lip_left_contour3"]
        # fw.write("%d %d\n"%((point1['x']+point2['x'])/2,(point1['y']+point2['y'])/2))

        rect=face["face_rectangle"]
        box=doc.createElement("box")
        box.setAttribute("top",str(rect['top']))
        box.setAttribute("left", str(rect['left']))
        box.setAttribute("width", str(rect['width']))
        box.setAttribute("height", str(rect['height']))

        parts=fw.get_parts()
        for part in parts:
            box.appendChild(part)
        image.appendChild(box)
    return image


images=doc.createElement("images")
def solve(root_path):
    file_list=os.listdir(root_path)
    for file in file_list:
        (name,extension) = os.path.splitext(file)
        if extension == '.bmp':
            continue
        file_path=os.path.join(root_path,file)
        if os.path.isdir(file_path):
            solve(file_path)
        else:
            print(file_path)
            fh = open(file_path, 'r')
            result = fh.read()
            fh.close()
            req_dict = json.JSONDecoder().decode(result)
            image=create_image_element(req_dict)
            if image is None:
                continue
            image_path=file_path.replace(".json","").replace("json","IR")
            image.setAttribute("file",image_path)
            images.appendChild(image)
    return images




def main():
    root_dir="E://colleague//dealfiles//kevin//smoke//1xiao"



    os.chdir(root_dir)

    dataset=doc.createElement("dataset")
    name=doc.createElement("name")
    name_text=doc.createTextNode("Training face")
    name.appendChild(name_text)
    dataset.appendChild(name)

    comment=doc.createElement("comment")
    comment_text=doc.createTextNode("Create by Shuhao Yuan")
    comment.appendChild(comment_text)
    dataset.appendChild(comment)



    my_images=solve(root_dir)
    dataset.appendChild(my_images)


    with open('test.xml', 'w') as f:
        f.write("<?xml version='1.0' encoding='ISO-8859-1'?>\n")
        f.write("<?xml-stylesheet type='text/xsl' href='image_metadata_stylesheet.xsl'?>\n")
        dataset.writexml(f, addindent=' ', newl='\n')

    



def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print("copy %s -> %s"%( srcfile,dstfile))

if __name__=='__main__':
    main()
