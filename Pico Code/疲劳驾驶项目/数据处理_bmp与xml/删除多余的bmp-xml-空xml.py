
# coding: utf-8

# In[1]:


from xml.dom.minidom import parse
import xml.dom.minidom
import os
import shutil


# ## 输入原始路径，下面存放多个标记好的文件夹

# In[9]:


path = 'E:\\ImgeLabel\\data\\test'
filelists = os.listdir(path)

move_path='E:\\move_picture'


if not os.path.exists(move_path):
    os.mkdir(move_path)


# ### 删除多余的bmp文件

# In[34]:

def del_bmp_jpg():
    for file1 in filelists:
    	path1 = os.path.join(path,file1)
    	listfiles2 = os.listdir(path1)
    	for file2 in listfiles2:
    		path2 = os.path.join(path1,file2)
    		(name1,extension1) = os.path.splitext(file2)
    		if extension1 == '.jpg':
    			path3 = os.path.join(path1,name1+'.xml')
    			if not os.path.isfile(path3):
    				print(path2)
    				shutil.move(path2,move_path)
                    # os.remove(path2)

def del_xml():
    for file1 in filelists:
        path1 = os.path.join(path,file1)
        listfiles2 = os.listdir(path1)
        for file2 in listfiles2:
            path2 = os.path.join(path1,file2)
            (name1,extension1) = os.path.splitext(file2)
            if extension1 == '.xml':
                path3 = os.path.join(path1,name1+'.jpg')
                if not os.path.isfile(path3):
                    print(path2)
                    shutil.move(path2,move_path)
                    # os.remove(path2)


# ### 删除空xml文件

# In[36]:
filelists0 = os.listdir(path)

def del_xml_bmljpg():
    for file2 in filelists0:
        path_1 = os.path.join(path,file2)
        filelists1 = os.listdir(path_1)
        for file3 in filelists1:
            (name2,extension2) = os.path.splitext(file3)
            path_2 = os.path.join(path_1,name2+'.jpg')
            path_3 = os.path.join(path_1,file3)
            if extension2 == '.xml':
                test1 = parse(path_3)
                content1 = test1.documentElement
                if len(content1.getElementsByTagName('object')) == 0:
                    print(path_2)
                    print(path_3)
                    shutil.move(path_2,move_path)
                    shutil.move(path_3,move_path)
                    # os.remove(path_2)
                    # os.remove(path_3)
                #namelabel = content1.getElementsByTagName('name')
                #if namelabel[0].firstChild.data == 'smoke':#判断打电话中是否有抽烟
                    # print(path_2)
                    # print(path_3)

if __name__ == '__main__':
    del_bmp_jpg()
    del_xml()
    del_xml_bmljpg()
