import os
import pandas as pd
import shutil

#服务器csv地址
path1 = "H:\\Tidy_delete_bmp\\delete_bmp_smoke0528"

#服务器bmp地址
path1_1 = "H:\\Smoking0528"

for file1 in listfiles1:
    path2 = os.path.join(path1,file1)
    path2_1 = os.path.join(path1_1,file1)
    listfiles2 = os.listdir(path2)
    for file2 in listfiles2:
        (name1,extension1) = os.path.splitext(file2)
        path3 = os.path.join(path2,file2)
        path3_1 = os.path.join(path2_1,name1)
        data = pd.read_csv(path3)
        num1 = data.shape[0]
        for i in range(num1):
            path4_1 = os.path.join(path3_1,str(data["deletebmp"][i]))
            print(path4_1)
            #os.remove(path4_1)
