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


data_dir = '/data/aaron/yolotest/darknet/data/testdata2/hardData/G1/hardData/0/'

xml_dir = '/data/aaron/yolotest/darknet/data/testdata2/xml/G1/0/'

output_dir = '/data/aaron/yolotest/darknet/data/out/'

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



#lib = CDLL("/media/pico/886835D26835C02C/Kevin_ubuntu/darknet/libdarknet.so", RTLD_GLOBAL)
lib = CDLL("libdarknet.so", RTLD_GLOBAL)
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

def draw_boxes(result, im_path):
    image = cv2.imread(os.path.join(data_dir, im_path), cv2.IMREAD_COLOR)
    for i in range(len(result)):
    #    print(i, ':', result[i][2])
        x, y = result[i][2][0], result[i][2][1]
        w, h = result[i][2][2],result[i][2][3]

        cv2.rectangle(image, (int(x - w / 2), int(y - h / 2) ), (int(x + w / 2), int(y + h / 2)), (0,255,0), 2)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(image, str(result[i][0].decode()).capitalize(), (int(x), int(y)), font, 1e-3*724, (0,0,223), 2, cv2.LINE_AA)
    cv2.imwrite(os.path.join(output_dir, im_path), image)


def write_xml(result,im_path):

    for i in range(len(result)):
    #    print(i, ':', result[i][2])
        x, y = result[i][2][0], result[i][2][1]
        w, h = result[i][2][2],result[i][2][3]
        xmin1 = int(x - w / 2)
        ymin1 = int(y - h / 2)
        xmax1 = int(x + w / 2)
        ymax1 = int(y + h / 2)
        label1 = str(result[i][0].decode())

        path_xml = "/data/aaron/yolotest/1.xml"
        xml1 = parse(path_xml)
        content_xml = xml1.documentElement

        xml_xmin = content_xml.getElementsByTagName('xmin')
        xmin = xml_xmin[0]
        xmin.firstChild.data = xmin1
        xml_xmax = content_xml.getElementsByTagName('xmax')
        xmax = xml_xmax[0]
        xmax.firstChild.data = xmax1
        xml_ymin = content_xml.getElementsByTagName('ymin')
        ymin = xml_ymin[0]
        ymin.firstChild.data = ymin1
        xml_ymax = content_xml.getElementsByTagName('ymax')
        ymax = xml_ymax[0]
        ymax.firstChild.data = ymax1
        xml_label = content_xml.getElementsByTagName('name')
        label = xml_label[0]
        label.firstChild.data = label1
        xml_filename = content_xml.getElementsByTagName('filename')
        filename = xml_filename[0]
        filename.firstChild.data = im_path

        xml_name = str(img_path).split('.')[0]


        with open(os.path.join(xml_dir,xml_name+".xml"),'w') as fh:
            xml1.writexml(fh)





def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
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

if __name__ == "__main__":


    net = load_net("/data/aaron/yolotest/darknet/cfg/yolov3-voc.cfg", "/data/aaron/yolotest/darknet/backup/yolov3-voc_30000.weights", 0)
    meta = load_meta("/data/aaron/yolotest/darknet/cfg/hgr.data")
    total_pred_time = 0
    img_paths = os.listdir(data_dir)
    img_paths = sorted(img_paths)
    total_time_taken = 0
    for img_path in img_paths:
        tick = time()
        r, pred_time = detect(net, meta, str.encode(os.path.join(data_dir, img_path)))
        tock = time()
        total_pred_time += pred_time
        total_time_taken += tock-tick
        #draw_boxes(r, img_path)
        write_xml(r,img_path)
        print('Time taken: {}sec,\nResult: {}'.format(tock-tick, r))
    print('FPS for prediction : {}\nFPS for total process : {}'.format(float(len(img_paths)/total_pred_time),
         float(len(img_paths)/total_time_taken)))

    # print(np.asarray(r).shape)
	

print("Done!!")



