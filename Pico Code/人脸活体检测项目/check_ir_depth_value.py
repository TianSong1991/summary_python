import os
import cv2

depth_path = '/***/depth/'

ir_path = '/***/ir/'

def print_ir_value(path1):

	for file1 in os.listdir(path1):

		image_path = os.path.join(path1,file1)

		image1 = cv2.imread(image_path,-1)

		ir = cv2.split(image1)[0]

		print("max ir:",ir.max())

		print("min ir:",ir.min())

	print("IR is Done!")


def print_depth_value(path1):

	for file1 in os.listdir(path1):

		image_path = os.path.join(path1,file1)

		depth = cv2.imread(image_path,-1)

		print(depth.max(),depth.min())

	print("Depth is Done!")


if __name__ == '__main__':
	#print_depth_value(depth_path)
	print_ir_value(ir_path)