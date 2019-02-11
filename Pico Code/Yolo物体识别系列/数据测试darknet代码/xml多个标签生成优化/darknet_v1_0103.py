# -*- coding:utf-8 -*-
import os
import cv2
import shutil
from xml.dom.minidom import parse
import xml.dom.minidom
import xml.etree.ElementTree as ET

test1 = '/home/pico/001337.xml'


xml3 = ET.parse(test1)
xml3_1 = xml3.getroot()

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

xml2_name.text = 'abc'
xml2_pose.text = 'Unspecified'
xml2_truncated.text = str(0)
xml2_difficult.text = str(0)
xml2_bndbox_xmin.text = str(10)
xml2_bndbox_ymin.text = str(12)
xml2_bndbox_xmax.text = str(13)
xml2_bndbox_ymax.text = str(14)

xml3_1.append(xml2)


xml3.write('/home/pico/test1.xml')
