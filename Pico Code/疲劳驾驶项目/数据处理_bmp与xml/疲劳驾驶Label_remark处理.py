
# coding: utf-8

# In[1]:


from xml.dom.minidom import parse
import xml.dom.minidom
import os
import shutil


# ## 输入原始路径，下面存放多个标记好的文件夹

# In[9]:


path = 'E:\\colleague\\smoke2'
filelists = os.listdir(path)


# ### 删除多余的bmp文件

# In[34]:


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

for file1 in filelists:
    path1 = os.path.join(path,file1)
    listfiles2 = os.listdir(path1)
    for file2 in listfiles2:
        path2 = os.path.join(path1,file2)
        (name1,extension1) = os.path.splitext(file2)
        if extension1 == '.xml':
            path3 = os.path.join(path1,name1+'.bmp')
            if not os.path.isfile(path3):
                print(path2)
                os.remove(path2)


# ### 删除空xml文件

# In[36]:


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


# ## 将同时标记phone和smoke的文件进行转移，转移路径如下，记得每次运行修改

# In[ ]:


path_new = "E:\\colleague\\smoke_phone1"


# ### 开始移动，判定标注是有两个label

# In[23]:


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
            if len(content1.getElementsByTagName('object')) == 2:
                print(path_2)
                print(path_3)
                shutil.move(path_2,path_new)
                shutil.move(path_3,path_new)


# ## 对只有一个标签的，将打电话的进行移动

# In[6]:


path_phone = "E:\\colleague\\phone1"


# ### 开始移动打电话的数据，剩下的都是抽烟的数据

# In[12]:


for file2 in filelists:
    path_1 = os.path.join(path,file2)
    filelists1 = os.listdir(path_1)
    for file3 in filelists1:
        (name2,extension2) = os.path.splitext(file3)
        path_2 = os.path.join(path_1,name2+'.bmp')
        path_3 = os.path.join(path_1,file3)
        if extension2 == '.xml':
            test2 = parse(path_3)
            content2 = test2.documentElement
            namelabel = content2.getElementsByTagName('name')
            if namelabel[0].firstChild.data == 'phone':
                print(path_2)
                print(path_3)
                shutil.move(path_2,path_phone)
                shutil.move(path_3,path_phone)

