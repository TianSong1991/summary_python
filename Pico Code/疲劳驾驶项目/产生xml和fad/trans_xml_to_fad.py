#!/bin/python2
#-*- coding: utf-8 -*-
# Author: Shuhao Yuan (袁书豪)
# Date  : 2018/8/17
# Email : 294663908@qq.com

import json
import os
import shutil
from xml.dom import minidom
import re

root_dir = "E://colleague//dealfiles//kevin//smoke//part"

for file in os.listdir(root_dir):
    path1 = os.path.join(root_dir,file)
    os.chdir(path1)

#os.chdir(root_dir)



    def getConnectionsById(id):
        doc=minidom.Document()
        Connections=doc.createElement("Connections")

        indexs=[16,21,26,30,35,41,47,59,67]
        for index in indexs:
            if id==index:
                return  Connections

        if id==48:
            Target = doc.createElement("Target")
            Target.setAttribute("id", "%d" % ( 59))
            Connections.appendChild(Target)
        elif id==60:
            Target = doc.createElement("Target")
            Target.setAttribute("id", "%d" % ( 67))
            Connections.appendChild(Target)
        elif id == 36:
            Target = doc.createElement("Target")
            Target.setAttribute("id", "%d" % (41))
            Connections.appendChild(Target)
        elif id == 42:
            Target = doc.createElement("Target")
            Target.setAttribute("id", "%d" % (47))
            Connections.appendChild(Target)


        Target = doc.createElement("Target")
        Target.setAttribute("id", "%d" % ((id + 1) % 68))
        Connections.appendChild(Target)

        return Connections

    def part2Feature(part):
        doc=minidom.Document()
        Feature=doc.createElement("Feature")

        name=part.getAttribute("name")
        id=int(name)
        x=part.getAttribute("x")
        y = part.getAttribute("y")
        Connections=getConnectionsById(id)

        Feature.setAttribute("id","%d"%(id))
        Feature.setAttribute("x",x)
        Feature.setAttribute("y",y)
        Feature.appendChild(Connections)
        return Feature


    def box2Features(box):
        doc = minidom.Document()
        Features=doc.createElement("Features")

        part_list=box.getElementsByTagName("part")
        for part in part_list:
            Feature=part2Feature(part)
            Features.appendChild(Feature)

        return Features


    def image2Sample(image):
        doc = minidom.Document()
        Sample=doc.createElement("Sample")
        fileName=image.getAttribute("file")
        Sample.setAttribute("fileName",fileName)
        box_list=image.getElementsByTagName("box")
        for box in box_list:
            Features=box2Features(box)
            Sample.appendChild(Features)
        return Sample

    def images2Samples(images):
        doc=minidom.Document()
        Samples=doc.createElement("Samples")
        image_list=images.getElementsByTagName("image")
        for image in image_list:
            Sample=image2Sample(image)
            Samples.appendChild(Sample)
        return Samples


    def trans(xml_path):
        dom=minidom.parse(xml_path)
        doc=minidom.Document()
        FaceDataset=doc.createElement("FaceDataset")
        FaceDataset.setAttribute("xmlns","https://github.com/luigivieira/Facial-Landmarks-Annotation-Tool")
        FaceDataset.setAttribute("numberOfFeatures","68")

        images=dom.getElementsByTagName("images")[0]
        Samples=images2Samples(images)
        FaceDataset.appendChild(Samples)

        return FaceDataset








    FaceDataset=trans("./test.xml")
    print(FaceDataset.toprettyxml(encoding="utf-8"))
    f=open("./test.fad","wb")
    f.write(FaceDataset.toprettyxml(encoding="utf-8"))
    f.close()
