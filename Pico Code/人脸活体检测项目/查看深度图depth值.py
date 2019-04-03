import os
import cv2
depth_path = '/media/pico/data/Project_FaceDetection/Data_Tengxun/01_Original_data/stronglight/data0214/name1/depth/'


def print_depth_value(path1):

	for file1 in os.listdir(path1):
		image_path = os.path.join(path1,file1)
		depth = cv2.imread(image_path,-1)

		#depth = cv2.split(image1)[0]
		data = []
		for i in range(480):
			for j in range(640):
				if depth[i,j] > 0:
					data.append(depth[i,j])
					#print(depth[i,j])

		print("max depth:",max(data))

		print("min depth:",min(data))

if __name__ == '__main__':
	print_depth_value(depth_path)