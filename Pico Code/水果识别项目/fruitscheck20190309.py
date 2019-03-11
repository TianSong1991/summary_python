# -*- coding:utf-8 -*-

from ctypes import *
import math
import random
import cv2
from time import time
import os
import numpy as np
from xml.dom.minidom import parse
import xml.dom.minidom
import shutil
import xml.etree.ElementTree as ET

data_dir = '***'

outimgpath = '***'



def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1

def c_array(ctype, values):
    arr = (ctype*len(values))()
    arr[:] = values
    return arr

class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]

class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]



lib = CDLL("***/python/libdarknet.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res

def draw_boxes(result, im_path,outim_path):
    image = cv2.imread(im_path, cv2.IMREAD_COLOR)
    for i in range(len(result)):
    #    print(i, ':', result[i][2])
        x, y = result[i][2][0], result[i][2][1]
        w, h = result[i][2][2],result[i][2][3]

        cv2.rectangle(image, (int(x - w / 2), int(y - h / 2) ), (int(x + w / 2), int(y + h / 2)), (0,255,0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, str(result[i][0].decode()).capitalize(), (int(x), int(y)), font, 1e-3*724, (0,0,223), 2)
    suffix=os.path.split(im_path)  #分割文件名
    cv2.imwrite(os.path.join(outim_path,suffix[1]), image)


def write_xml(result,file_path,outim_path):
	#result是预测的结果，filepath是图像文件的全路径，outim—_path是要保存的文件夹
    imgname=os.path.split(file_path)
    img_path=imgname[1]   #提取图像文件的文件名

    path_xml = "***/Picture1.xml"#直接读取一个适合labelimg的xml文件，并在其下面进行修改，然后保存即可
    xml3 = ET.parse(path_xml)
    xml3_1 = xml3.getroot()
    for i in range(len(result)):
        x, y = result[i][2][0],result[i][2][1]
        w, h = result[i][2][2],result[i][2][3]
        xmin1 = int(x - w / 2)
        ymin1 = int(y - h / 2)
        xmax1 = int(x + w / 2)
        ymax1 = int(y + h / 2)
        label1 = str(result[i][0].decode())

        xml2 = ET.Element('object')
        xml2_name = ET.SubElement(xml2,'name')
        xml2_pose = ET.SubElement(xml2,'pose')
        xml2_truncated = ET.SubElement(xml2,'truncated')
        xml2_difficult = ET.SubElement(xml2,'difficult')
        xml2_bndbox = ET.SubElement(xml2,'bndbox')
        xml2_bndbox_xmin = ET.SubElement(xml2_bndbox,'xmin')
        xml2_bndbox_ymin = ET.SubElement(xml2_bndbox,'ymin')
        xml2_bndbox_xmax = ET.SubElement(xml2_bndbox,'xmax')
        xml2_bndbox_ymax = ET.SubElement(xml2_bndbox,'ymax')

        xml2_name.text = str(label1)
        xml2_pose.text = 'Unspecified'
        xml2_truncated.text = str(0)
        xml2_difficult.text = str(0)
        xml2_bndbox_xmin.text = str(xmin1)
        xml2_bndbox_ymin.text = str(ymin1)
        xml2_bndbox_xmax.text = str(xmax1)
        xml2_bndbox_ymax.text = str(ymax1)

        xml3_1.append(xml2)

		
        xml_name = str(img_path).split('.')[0]


        with open(os.path.join(outim_path,xml_name+".xml"),'w') as fh:
            xml3.write(fh)





def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    print(image)
    im = load_image(image, 0, 0)
    num = c_int(0)
    pnum = pointer(num)
    start_time = time()
    predict_image(net, im)
    pred_time = time() - start_time
    dets = get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
    num = pnum[0]
    if (nms): do_nms_obj(dets, num, meta.classes, nms);

    res = []
    for j in range(num):
        for i in range(meta.classes):
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_detections(dets, num)
    return res, pred_time

def travers(imgpath,outimgpath,imglist,crosspondoutimglist):  #imgpath是原始图片路径和文件名，outpath只有输出的文件路径
	if os.path.isdir(imgpath):
		for file1 in os.listdir(imgpath):
			imgpath1=os.path.join(imgpath,file1)
			outimgpath1=outimgpath    #此处只有当
			if os.path.isdir(imgpath1):
				outimgpath1=os.path.join(outimgpath1,file1)
				if not os.path.exists(outimgpath1):    #创建对应的img文件夹
					os.mkdir(outimgpath1)
			travers(imgpath1,outimgpath1,imglist,crosspondoutimglist)
	else:
		imglist.append(imgpath)
		crosspondoutimglist.append(outimgpath)


if __name__ == "__main__":


    net = load_net(b"***/yolov3-fruits.cfg", b"***/yolov3.weights", 0)
    meta = load_meta(b"***/fruits.data")
    total_pred_time = 0

    imglist=[]
    crosspondoutimglist=[]
    travers(data_dir,outimgpath,imglist,crosspondoutimglist)

    # = os.listdir(data_dir)
    #img_paths = sorted(img_paths)
    total_time_taken = 0
    for i,img_path in  enumerate(imglist):
        tick = time()
        #r, pred_time = detect(net, meta, str.encode(os.path.join(data_dir, img_path)))
        r, pred_time = detect(net, meta, img_path)
        tock = time()
        total_pred_time += pred_time
        total_time_taken += tock-tick
        draw_boxes(r, img_path,crosspondoutimglist[i])
        write_xml(r,img_path,crosspondoutimglist[i])
        print('Time taken: {}sec,\nResult: {}'.format(tock-tick, r))
# print('FPS for prediction : {}\nFPS for total process : {}'.format(float(len (img_paths)/total_pred_time),
        #float(len(img_paths)/total_time_taken)))

    #print(np.asarray(r).shape)
	

print("Done!!")



