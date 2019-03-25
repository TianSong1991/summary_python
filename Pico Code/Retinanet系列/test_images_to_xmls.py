# import keras
import keras

# import keras_retinanet
from keras_retinanet import models
from keras_retinanet.utils.image import read_image_bgr, preprocess_image, resize_image
from keras_retinanet.utils.visualization import draw_box, draw_caption
from keras_retinanet.utils.colors import label_color

# import miscellaneous modules
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np
import time
from xml.dom.minidom import parse
import xml.dom.minidom
import shutil
import xml.etree.ElementTree as ET
# set tf backend to allow memory to grow, instead of claiming everything
import tensorflow as tf


def get_session():
	config = tf.ConfigProto()
	config.gpu_options.allow_growth = True
	return tf.Session(config=config)

# use this environment flag to change which GPU to use
#os.environ["CUDA_VISIBLE_DEVICES"] = "1"

# set the modified tf session as backend in keras
keras.backend.tensorflow_backend.set_session(get_session())


# adjust this to point to your downloaded/trained model
# models can be downloaded here: https://github.com/fizyr/keras-retinanet/releases
model_path = os.path.join('/******/Kevin_ubuntu/Object_detection/keras-retinanet', 'snapshots', 'resnet50_csv_01.h5')

# load retinanet model
model = models.load_model(model_path, backbone_name='resnet50')

# if the model is not converted to an inference model, use the line below
# see: https://github.com/fizyr/keras-retinanet#converting-a-training-model-to-inference-model
#model = models.convert_model(model)

#print(model.summary())

# load label to names mapping for visualization purposes
labels_to_names = {0: 'apple', 1: 'pear', 2: 'strawberry'}

################################################################################
image_path = '/******/Kevin_ubuntu/data/myowndata/fruit_data/test'
datalist = []

def get_all_files(path1):
	files = os.listdir(path1)
	for file in files:
		file_path = os.path.join(path1,file)            
		if os.path.isdir(file_path):
			get_all_files(file_path)                  
		else:
			(name1,extension1) = os.path.splitext(file_path)
			if extension1 == '.jpg':
				datalist.append(file_path)
get_all_files(image_path)

# load image
for i in range(len(datalist)):
	image = read_image_bgr(datalist[i])

	# copy to draw on
	draw = image.copy()
	draw = cv2.cvtColor(draw, cv2.COLOR_BGR2RGB)

	# preprocess image for network
	image = preprocess_image(image)
	image, scale = resize_image(image)

	# process image
	start = time.time()
	boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
	print(datalist[i])

	# correct for image scale
	boxes /= scale

	# visualize detections
	path_xml = "/******/Kevin_ubuntu/data/Picture1.xml"
	xml3 = ET.parse(path_xml)
	xml3_1 = xml3.getroot()
	for box, score, label in zip(boxes[0], scores[0], labels[0]):
		# scores are sorted so we can break
		if score < 0.7:
			break

		color = label_color(label)

		b = box.astype(int)
		#draw_box(draw, b, color=color)

		#caption = "{} {:.3f}".format(labels_to_names[label], score)
		print(labels_to_names[label],b[0],b[1],b[2],b[3],score)
		xmin1 = b[0]
		ymin1 = b[1]
		xmax1 = b[2]
		ymax1 = b[3]
		label1 = str(labels_to_names[label])

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

		xml_name = str(datalist[i]).split('.')[0]
		print(xml3_1)


		with open(os.path.join(xml_name+".xml"),'wb') as fh:
			xml3.write(fh)

########################################
		#draw_caption(draw, b, caption)#
	# plt.figure(figsize=(15, 15))     #
	# plt.axis('off')                  #
	# plt.imshow(draw)                 #
	# plt.show()                       #
########################################

