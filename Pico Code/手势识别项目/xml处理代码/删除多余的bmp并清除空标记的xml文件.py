from xml.dom.minidom import parse
import xml.dom.minidom
import os
import shutil


path = 'E:\\colleague\\dealfiles\\kevin\\smoke'

filelists = os.listdir(path)


for file1 in filelists:
	path1 = os.path.join(path,file1)
	listfiles2 = os.listdir(path1)
	for file2 in listfiles2:
		path2 = os.path.join(path1,file2)
		(name1,extension1) = os.path.splitext(file2)
		if extension1 == '.bmp':
			path3 = os.path.join(path1,name1+'.xml')
			if not os.path.isfile(path3):
				print(path2)
				os.remove(path2)


for file2 in filelists:
    path_1 = os.path.join(path,file2)
    filelists1 = os.listdir(path_1)
    for file3 in filelists1:
        (name2,extension2) = os.path.splitext(file3)
        path_2 = os.path.join(path_1,name2+'.bmp')
        path_3 = os.path.join(path_1,file3)
        if extension2 == '.xml':
            test1 = parse(path_3)
            content1 = test1.documentElement
            if len(content1.getElementsByTagName('object')) == 0:
                print(path_2)
                print(path_3)
                os.remove(path_2)
                os.remove(path_3)