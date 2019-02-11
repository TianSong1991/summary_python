import os
import pandas as pd
import shutil
import numpy as np

root_path = 'F:\\template\\handobj-mark\\data\\img'

copy_path = 'F:\\Right_vini'

os.makedirs(copy_path)

def delete_txt(root1):	
	os.chdir(root1)
	files = os.listdir(root1)
	data = pd.DataFrame(np.zeros(5000),columns = ['pngname'])
	data1 = pd.DataFrame(np.zeros(5000),columns = ['txtname'])
	i = 0
	j = 0
	for filename in files:
	    (name1,extension1) = os.path.splitext(filename)
	    if extension1 == '.png':
	        data['pngname'][i] = name1
	        i = i+1
	    else:
	        data1['txtname'][j] = name1
	        j = j+1
	datapng = data[data.pngname > 0]
	
	datatxt = data1[data1.txtname > 0]
	if datapng.shape[0] <= datatxt.shape[0]:
	    data2 = pd.merge(left=datatxt, right=datapng, how='left', left_on='txtname', right_on='pngname')
	    print('OK!')
	else:
	    data2 = pd.merge(left=datapng, right=datatxt, how='left', left_on='pngname', right_on='txtname')
	    print('Error!')
	data2["bz"] = data2["txtname"] - data2["pngname"]
	rmdata = pd.DataFrame(data2[data2.bz != 0]["txtname"].astype(np.int64).astype(np.str))
	rmdata["txtname"] = rmdata["txtname"] + '.txt'
	for i in rmdata.index:
	    rmfile = os.path.join(root_path,rmdata["txtname"][i])
	    os.remove(rmfile)

	delete_files(datapng)



def delete_files(datapng):
	num1 = 4492
	originaldata = pd.DataFrame(np.ones(num1),columns = ['original'])
	for i in range(1,num1):
	    originaldata["original"][i] = originaldata["original"][i] + originaldata["original"][i-1]
	result = pd.merge(left=originaldata, right=datapng, how='left', left_on='original', right_on='pngname')
	result["bz"] = result["original"] - result["pngname"]
	resultdata = result[result.bz != 0]
	result1 = resultdata["original"].astype(np.int64).astype(np.str)
	result1 = pd.DataFrame(result1)
	result1["original"] = result1["original"] + '.png'

	result1.to_excel("F:\\delete_vini.xlsx",index = False)




def copy_files(path1,path2):
    label_files = os.listdir(path1)
    for label_file in label_files:
        (name,extension) = os.path.splitext(label_file)
        if extension == '.txt':
            textfile_path = os.path.join(path1,label_file)
            shutil.copy(textfile_path,path2)

if __name__=='__main__':

	delete_txt(root_path)

	copy_files(root_path,copy_path)

