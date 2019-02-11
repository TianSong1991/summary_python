import os
import pandas as pd
import shutil
import numpy as np
import zipfile

#程序只需要修改一个地方
# 修改一，需要修改root_path为原始文件路径

os.chdir("E:\\")

root_path = 'E:\\ImgeLabel\\data\\7'

(zippath0,test0) = os.path.split(root_path)

copy_path = "E:" + "\\" + str(test0) + "\\" + "xml"

(zippath1,test1) = os.path.split(copy_path)

(zippath2,test2) = os.path.split(zippath1)

if not os.path.exists(copy_path):
    os.makedirs(copy_path)



def move_files(path1,path2):
    label_files = os.listdir(path1)
    for label_file in label_files:
        (name,extension) = os.path.splitext(label_file)
        if extension == '.xml':   
            textfile_path = os.path.join(path1,label_file)
            shutil.move(textfile_path,path2)


def read_files(path3,path4):
    i = 0 
    data_xml = pd.DataFrame(np.zeros(10000),columns = ['xmlname'])
    for xml_file in os.listdir(path3):
         (name1,extension1) = os.path.splitext(xml_file)
         data_xml['xmlname'][i] = name1
         i = i + 1
    data_xml = data_xml[data_xml.xmlname > 0]
    j = 0 
    data_jpg = pd.DataFrame(np.zeros(10000),columns = ['jpgname'])
    for jpg_file in os.listdir(path4):
         (name2,extension2) = os.path.splitext(jpg_file)
         data_jpg['jpgname'][j] = name2
         j = j + 1
    data_jpg = data_jpg[data_jpg.jpgname > 0]
    data = pd.merge(left=data_jpg, right=data_xml, how='left', left_on='jpgname', right_on='xmlname')
    data["rm"] = data["jpgname"] - data["xmlname"]
    rmdata = pd.DataFrame(data[data.rm != 0]["jpgname"].astype(np.int64).astype(np.str))
    rmdata["jpgname"] = rmdata["jpgname"] + '.jpg'
    for i in rmdata.index:
        rmfile = os.path.join(path4,rmdata["jpgname"][i])
        print(rmfile)
        #os.remove(rmfile)

    rmdata.to_excel(zippath1 + "\\" + str(test2)+".xlsx",index = False)



if __name__=='__main__':

    move_files(root_path,copy_path)

    read_files(copy_path,root_path)


    shutil.make_archive(str(test2),"zip",zippath1)#第一个参数0是压缩包后的名称，第二个参数zip是压缩成zip格式压缩包，第三个参数是压缩路径。

