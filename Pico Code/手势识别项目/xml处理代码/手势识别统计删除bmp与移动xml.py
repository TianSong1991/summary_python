import os
import pandas as pd
import shutil
import numpy as np

#程序只需要修改两个地方，为修改一和修改二，修改一修改路径根据自己的实际情况修改，修改二为保存自己删除的图片的Excel
# 修改一，需要修改root_path为原始文件路径，copy_path为你要提取的xml或者txt路径

root_path = 'E:\\colleague\\dealfiles\\kevin\\G1\\0'

copy_path = 'E:\\0\\xml'

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
    num1 = len(os.listdir(path4))
    originaldata = pd.DataFrame(np.ones(num1),columns = ['original'])
    for i in range(1,num1):
        originaldata["original"][i] = originaldata["original"][i] + originaldata["original"][i-1]
    data = pd.merge(left=originaldata, right=data_xml, how='left', left_on='original', right_on='xmlname')
    data["rm"] = data["original"] - data["xmlname"]
    rmdata = pd.DataFrame(data[data.rm != 0]["original"].astype(np.int64).astype(np.str))
    rmdata["original"] = rmdata["original"] + '.jpg'
    for i in rmdata.index:
        rmfile = os.path.join(path4,rmdata["original"][i])
        os.remove(rmfile)
    #修改二
    #对删除的文档保存在Excel文档中并重新命名。
    rmdata.to_excel("E:\\0\\0.xlsx",index = False)




if __name__=='__main__':

    move_files(root_path,copy_path)

    read_files(copy_path,root_path)

