# -*- coding:utf-8 -*-
import os
import shutil
import hashlib
import cv2
import numpy as np

path1 = 'K:\\Tiger20190227'

#path2 = 'I:\\Project_FaceDetection\\Data_Tengxun\\02_Tidy_data\\data0215'

path2 = 'G:\\侧光150人数据'



creatpath = 'G:\\Project_face_detection\\sidelight_tidy'

# path_0 = 'H:\\活体检测'

# rename_path = '/media/pico/新加卷/活体检测/data3/positive_0131/test'

# path3 = 'I:\\test\\name30'
# path4 = 'I:\\test\\name29'
# path5 = 'I:\\人脸活体检测\\2019\\data0117\\data\\image_20190121_positive_part5'
# path6 = 'I:\\合格活体采集者'
# nullpath = 'D:\\活体检测负样本数据old'

#将过滤好的图片进行移动
def move_files(path1,path2):
	for file1 in os.listdir(path1):
		rgb_path = os.path.join(path1,file1,'rgb','new')
		depth_path = os.path.join(path1,file1,'depth')
		ir_path = os.path.join(path1,file1,'ir')
		
		n = 1
		if os.path.exists(rgb_path):
			num1 = len(os.listdir(rgb_path))
			for file2 in os.listdir(rgb_path):
				(name1,extension1) = os.path.splitext(file2)
				rgb_path1 = os.path.join(rgb_path,file2)
				depth_path1 = os.path.join(depth_path,name1+".png")
				ir_path1 = os.path.join(ir_path,name1+".png")
				movergb_path1 = os.path.join(path2,file1,"rgb","0"*(8-len(str(n)))+str(n)+".jpg")
				movedepth_path1 = os.path.join(path2,file1,"depth","0"*(8-len(str(n)))+str(n)+".png")
				moveir_path1 = os.path.join(path2,file1,"ir","0"*(8-len(str(n)))+str(n)+".png")
				n = n + 1
				shutil.copyfile(rgb_path1,movergb_path1)
				shutil.copyfile(depth_path1,movedepth_path1)
				shutil.copyfile(ir_path1,moveir_path1)


def move_files2(path1,path2,path3):
	for file1 in os.listdir(path2):
		rgb_path = os.path.join(path2,file1,'rgb')
		depth_path = os.path.join(path1,file1,'depth')
		ir_path = os.path.join(path1,file1,'ir')
		
		n = 1
		if os.path.exists(rgb_path):
			num1 = len(os.listdir(rgb_path))
			for file2 in os.listdir(rgb_path):
				(name1,extension1) = os.path.splitext(file2)
				rgb_path1 = os.path.join(rgb_path,file2)
				depth_path1 = os.path.join(depth_path,name1+".png")
				ir_path1 = os.path.join(ir_path,name1+".png")
				movergb_path1 = os.path.join(path3,file1,"rgb","0"*(8-len(str(n)))+str(n)+".jpg")
				movedepth_path1 = os.path.join(path3,file1,"depth","0"*(8-len(str(n)))+str(n)+".png")
				moveir_path1 = os.path.join(path3,file1,"ir","0"*(8-len(str(n)))+str(n)+".png")
				n = n + 1
				shutil.copyfile(rgb_path1,movergb_path1)
				shutil.copyfile(depth_path1,movedepth_path1)
				shutil.copyfile(ir_path1,moveir_path1)

#创建需要移动的文件夹
def make_paths(creatpath):
	for i in range(1,108):
		newpath = os.path.join(creatpath,"name"+str(i))
		newpath1 =os.path.join(newpath,'depth')
		newpath2 =os.path.join(newpath,'ir')
		newpath3 =os.path.join(newpath,'rgb')
		os.makedirs(newpath1)
		os.makedirs(newpath2)
		os.makedirs(newpath3)

#删除形成的new文件夹
def delete_files(path1):
	for file1 in os.listdir(path1):
		rgb_path = os.path.join(path1,file1,'rgb','new')
		depth_path = os.path.join(path1,file1,'depth','new')
		ir_path = os.path.join(path1,file1,'ir','new')
		if os.path.exists(rgb_path):
			shutil.rmtree(rgb_path)
			#shutil.rmtree(depth_path)
			#shutil.rmtree(ir_path)
			print(rgb_path)


#检测rgb、ir、depth数量是否一致
def check_num(path2):

	for file1 in os.listdir(path2):
		rgblist = []
		depthlist = []
		irlist = []
		move_path_1 = os.path.join(path2,file1)
		move_path_depth =os.path.join(move_path_1,'depth')
		move_path_ir =os.path.join(move_path_1,'ir')
		move_path_rgb =os.path.join(move_path_1,'rgb')
		num_depth = len(os.listdir(move_path_depth))
		num_ir = len(os.listdir(move_path_ir))
		num_rgb = len(os.listdir(move_path_rgb))
		for file2 in os.listdir(move_path_rgb):
			(name2,extension2) = os.path.splitext(file2)
			rgblist.append(int(name2))
		for file3 in os.listdir(move_path_depth):
			(name3,extension3) = os.path.splitext(file3)
			depthlist.append(int(name3))
		for file4 in os.listdir(move_path_ir):
			(name4,extension4) = os.path.splitext(file4)
			irlist.append(int(name4))
		#print(file1)

		if num_depth == num_ir == num_rgb == max(rgblist) == max(depthlist) == max(irlist):
			print(file1,num_rgb)
		else:
			print("error")
#重命名
def rename_files(rename_path):
	for file1 in os.listdir(rename_path):
		n = 1
		path_rgb = os.path.join(rename_path,file1,'rgb')
		path_depth = os.path.join(rename_path,file1,'depth')
		path_ir = os.path.join(rename_path,file1,'ir')
		for file2 in os.listdir(path_rgb):
			(name1,extension1) = os.path.splitext(file2)
			new_rgb_name = os.path.join(path_rgb,"0"*(8-len(str(n)))+str(n)+".jpg")
			new_depth_name = os.path.join(path_depth,"0"*(8-len(str(n)))+str(n)+".png")
			new_ir_name = os.path.join(path_ir,"0"*(8-len(str(n)))+str(n)+".png")
			path_rgb1 = os.path.join(path_rgb,file2)
			path_depth1 = os.path.join(path_depth,name1+".png")
			path_ir1 = os.path.join(path_ir,name1+".png")
			n = n + 1
			os.rename(path_rgb1,new_rgb_name)
			os.rename(path_depth1,new_depth_name)
			os.rename(path_ir1,new_ir_name)



#合并两个文件夹，用于数量不足的补充
def copy_add_file(path3,path4):
	rgb_path1 = os.path.join(path3,'rgb')
	depth_path1 = os.path.join(path3,'depth')
	ir_path1 = os.path.join(path3,'ir')
	num1 = len(os.listdir(rgb_path1)) + 1
	for file1 in os.listdir(os.path.join(path4,'rgb')):
		(name1,extension1) = os.path.splitext(file1)
		print(file1)
		move_rgb_path = os.path.join(path4,'rgb',file1)
		move_depth_path = os.path.join(path4,'depth',name1+".png")
		move_ir_path = os.path.join(path4,'ir',name1+".png")
		path3_rgb = os.path.join(rgb_path1,"0"*(8-len(str(num1)))+str(num1)+".jpg")
		path3_depth = os.path.join(depth_path1,"0"*(8-len(str(num1)))+str(num1)+".png")
		path3_ir = os.path.join(ir_path1,"0"*(8-len(str(num1)))+str(num1)+".png")
		print(path3_rgb,path3_depth,path3_ir)
		num1 = num1 + 1
		print("mum1:",num1)
		shutil.copyfile(move_rgb_path,path3_rgb)
		shutil.copyfile(move_depth_path,path3_depth)
		shutil.copyfile(move_ir_path,path3_ir)

#提取合格活体检测者
def get_people(path5,path6):
	n = 1
	for file1 in os.listdir(path5):
		path_rgb = os.path.join(path5,file1,'rgb')
		move_image_rgb = os.path.join(path_rgb,"0"*(8-len(str(n)))+str(n)+".jpg")
		n = n + 1
		shutil.copy(move_image_rgb,path6)

#文件夹重命名
renamepath = 'G:\\Project_face_detection\\backlight2_tidy'
def rename_file(renamepath):
	num1 = len(os.listdir(renamepath))
	n = 63
	for file1 in os.listdir(renamepath):
		os.rename(os.path.join(renamepath,file1),os.path.join(renamepath,"name"+str(n)))
		n = n + 1 

#判断文件夹是否为空
def null_file(nullpath):
	for file1 in os.listdir(nullpath):
		delele_path = os.path.join(nullpath,file1)
		path2 = os.path.join(nullpath,file1,'rgb')
		num1 = len(os.listdir(path2))
		if num1 == 0:
			print(delele_path,num1)
			shutil.rmtree(delele_path)

#check move path numbers
def check_move_path(path1):
	for file1 in os.listdir(path1):
		path2 = os.path.join(path1,file1,'rgb','new')
		if not os.path.exists(path2):
			print("error")
		else:
			num1 = len(os.listdir(path2))
			print(file1,":",num1)

#check all file number and print sum files
def check_num_sum(path_0):

	m = 0

	for file0 in os.listdir(path_0):

		move_path_0 = os.path.join(path_0,file0)
		
		for file1 in os.listdir(move_path_0):
			rgblist = []
			depthlist = []
			irlist = []
			move_path_1 = os.path.join(move_path_0,file1)

			move_path_depth =os.path.join(move_path_1,'depth')
			move_path_ir =os.path.join(move_path_1,'ir')
			move_path_rgb =os.path.join(move_path_1,'rgb')
			num_depth = len(os.listdir(move_path_depth))
			num_ir = len(os.listdir(move_path_ir))
			num_rgb = len(os.listdir(move_path_rgb))
			for file2 in os.listdir(move_path_rgb):
				(name2,extension2) = os.path.splitext(file2)
				rgblist.append(int(name2))
			for file3 in os.listdir(move_path_depth):
				(name3,extension3) = os.path.splitext(file3)
				depthlist.append(int(name3))
			for file4 in os.listdir(move_path_ir):
				(name4,extension4) = os.path.splitext(file4)
				irlist.append(int(name4))
			#print(file1)

			if num_depth == num_ir == num_rgb == max(rgblist) == max(depthlist) == max(irlist):
				m = m + 1
				print(file0,file1,num_rgb)
			else:
				print("error")
	print(m)


#获得所有人的图片的第一张和最后一张，查看是否为同一个人

path_1 = 'H:\\活体检测\\positive_data3'

path_2 = 'H:\\活体检测\\check'

def get_first_last_pic(path_1,path_2):
	for file1 in os.listdir(path_1):
		path3 = os.path.join(path_1,file1)
		path3_rgb = os.path.join(path3,'rgb')
		num1 = len(os.listdir(path3_rgb))
		first_pic = os.path.join(path3_rgb,"0"*(8-len(str(1)))+str(1)+".jpg")
		last_pic = os.path.join(path3_rgb,"0"*(8-len(str(num1)))+str(num1)+".jpg")
		first_pic_1 = os.path.join(path_2,file1+"_1.jpg")
		last_pic_1 = os.path.join(path_2,file1+"_2.jpg")
		shutil.copyfile(first_pic,first_pic_1)
		shutil.copyfile(last_pic,last_pic_1)

#创建压缩文件夹

def create_yasuo_file(path2):

	for i in range(7,8):
		create_file = os.path.join(path2,"image_20190304_positive_part"+str(i))
		if not os.path.exists(create_file):
			os.makedirs(create_file)


#创建txt文件
def create_txt_file(path2):
	os.chdir(path2)
	for i in range(7,8):
		with open("image_20190304_positive_part"+str(i)+".txt","w") as f:
			pass

#获取压缩包MD5值
def get_MD5(path0):
	for i in range(3,11):
	    path0_1 = os.path.join(path0,"image_20190304_positive_part"+str(i)+".zip")
	    path0_2 = os.path.join(path0,"image_20190304_positive_part"+str(i)+".txt")
	    with open(path0_1,'rb') as f:
	        md5obj = hashlib.md5()
	        md5obj.update(f.read())
	        hash1 = md5obj.hexdigest()
	        hash2 = str(hash1).upper()
	        with open(path0_2,'w') as g:
	            g.write("MD5:"+hash2)
	        print("MD5:%s"%hash2)



#使用Paul提供的工具进行数据清洗函数
paul_path = 'G:\\Project_face_detection\\backlight2_tidy'

kevin_path = 'G:\\Project_face_detection\\backlight2'

def move_kevin_to_paul(path1,path2):
	def create_new_path(path3):
		path3_rgb = os.path.join(path3,'rgb')
		path3_ir = os.path.join(path3,'ir')
		path3_depth = os.path.join(path3,'depth')
		if not os.path.exists(path3_rgb):
			os.makedirs(path3_rgb)
			os.makedirs(path3_ir)
			os.makedirs(path3_depth)
		return path3_rgb,path3_ir,path3_depth
	def move_images(path4,path5):
		for image1 in os.listdir(path4):
			image1_path = os.path.join(path4,image1)
			shutil.move(image1_path,path5)

	for file1 in os.listdir(path1):
		path1_1 = os.path.join(path1,file1,'rename')
		if os.path.exists(path1_1):
			path1_rgb = os.path.join(path1_1,'rgb')
			path1_ir = os.path.join(path1_1,'ir')
			path1_depth = os.path.join(path1_1,'depth')
			path2_1 = os.path.join(path2,file1)
			path2_rgb,path2_ir,path2_depth = create_new_path(path2_1)
			move_images(path1_rgb,path2_rgb)
			move_images(path1_ir,path2_ir)
			move_images(path1_depth,path2_depth)


#使用Python显示rgb、ir、depth三种图片的数据清洗函数
def move_kevin_to_kevin1(path1,path2):
	def create_new_path(path3):
		path3_rgb = os.path.join(path3,'rgb')
		path3_ir = os.path.join(path3,'ir')
		path3_depth = os.path.join(path3,'depth')
		if not os.path.exists(path3_rgb):
			os.makedirs(path3_rgb)
			os.makedirs(path3_ir)
			os.makedirs(path3_depth)
	def move_images(path1,path2):
		for file1 in os.listdir(path1):
			rgb_path = os.path.join(path1,file1,'rgb')
			depth_path = os.path.join(path1,file1,'depth')
			ir_path = os.path.join(path1,file1,'ir')
			n = 1
			for file2 in os.listdir(rgb_path):
				(name1,extension1) = os.path.splitext(file2)
				rgb_path1 = os.path.join(rgb_path,file2)
				depth_path1 = os.path.join(depth_path,name1+".png")
				ir_path1 = os.path.join(ir_path,name1+".png")
				movergb_path1 = os.path.join(path2,file1,"rgb","0"*(8-len(str(n)))+str(n)+".jpg")
				movedepth_path1 = os.path.join(path2,file1,"depth","0"*(8-len(str(n)))+str(n)+".png")
				moveir_path1 = os.path.join(path2,file1,"ir","0"*(8-len(str(n)))+str(n)+".png")
				n = n + 1
				shutil.copyfile(rgb_path1,movergb_path1)
				shutil.copyfile(depth_path1,movedepth_path1)
				shutil.copyfile(ir_path1,moveir_path1)

	for file0 in os.listdir(path1):
		path2_1 = os.path.join(path2,file0)
		create_new_path(path2_1)
	move_images(path1,path2)

			
#打印清洗数据后的数量
def check_rename_num(path1):
	for file1 in os.listdir(path1):
		path1_1 = os.path.join(path1,file1,'rename','rgb')
		num1 = len(os.listdir(path1_1))
		if os.path.exists(path1_1):
			print("{}:{}".format(file1,num1))
		else:
			print("{} is not exists!".format(file1))

#移动delete文件到原始文件下
def move_delete_to_original(path0):
	def move_images(path1,path2):
		for file0 in os.listdir(path1):
			image_file = os.path.join(path1,file0)
			shutil.move(image_file,path2)
	for file1 in os.listdir(path0):
		path_delete_rgb = os.path.join(path0,file1,'delete','rgb')
		path_delete_ir = os.path.join(path0,file1,'delete','ir')
		path_delete_depth = os.path.join(path0,file1,'delete','depth')
		path_rgb = os.path.join(path0,file1,'rgb')
		path_ir = os.path.join(path0,file1,'ir')
		path_depth = os.path.join(path0,file1,'depth')
		if os.path.exists(path_delete_rgb):
			move_images(path_delete_rgb,path_rgb)
			move_images(path_delete_ir,path_ir)
			move_images(path_delete_depth,path_depth)

#删除delet文件与rename文件
def rm_delete_rename_files(path0):
	for file1 in os.listdir(path0):
		path_delete = os.path.join(path0,file1,'delete')
		path_rename = os.path.join(path0,file1,'rename')
		if os.path.exists(path_delete):
			shutil.rmtree(path_delete)
		if os.path.exists(path_rename):
			shutil.rmtree(path_rename)


#检查ir和depth文件夹下最后一张图片是否是ir图片和depth图片
def check_ir_depth(path1):
	def show_IR_Depth_img(IR_path1,Depth_path1):
	#########################IR#################################
		ir_num = len(os.listdir(IR_path1))
		depth_num = len(os.listdir(Depth_path1))

		ir_image = os.path.join(IR_path1,"0"*(8-len(str(ir_num)))+str(ir_num)+".png")
		depth_image = os.path.join(Depth_path1,"0"*(8-len(str(depth_num)))+str(depth_num)+".png")

		def contrast_brightness_image(src1, a, g):
		    h, w, ch = src1.shape
		    src2 = np.zeros([h, w, ch], src1.dtype)
		    dst = cv2.addWeighted(src1, a, src2, 1-a, g)
		    #cv2.imshow("con-bri-demo", dst)
		    return dst 

		irimg16 = cv2.imread(ir_image,cv2.IMREAD_ANYDEPTH)
		irimg8 = irimg16.reshape(480,640,1)
		img = contrast_brightness_image(irimg8, 20, 50)
		cv2.imshow(ir_image,img)
		############################Depth##################################
		depthimg16 = cv2.imread(depth_image,cv2.IMREAD_ANYDEPTH)
		#img8 = np.clip(img16,0,255).astype(np.uint8)
		depthimg8 = cv2.convertScaleAbs(depthimg16)
		cv2.imshow(depth_image,depthimg8)
		cv2.waitKey(0)
		cv2.destroyAllWindows()

	for file1 in os.listdir(path1):
		path1_rgb = os.path.join(path1,file1,'rgb')
		path1_ir = os.path.join(path1,file1,'ir')
		path1_depth = os.path.join(path1,file1,'depth')
		show_IR_Depth_img(path1_ir,path1_depth)



if __name__ == '__main__':
	#check_move_path(path1)
	#make_paths(creatpath)
	#rename_files(rename_path)
	#rename_file(renamepath)
	#move_files(path1,path2)
	#move_files2(path1,path2,path3)
	#delete_files(path1)
	#check_num(path2)
	#check_num_sum(path_0)
	#create_yasuo_file(path2)
	#create_txt_file(path2)
	get_MD5(path2)
	#move_kevin_to_paul(kevin_path,paul_path)
	#move_kevin_to_kevin1(path1,path2)
	#check_rename_num(path1)






