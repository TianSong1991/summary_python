import os
import zipfile

os.chdir('E:\\')

rootpath  = 'E:\\Data\\test'

def zipfun(zippath):
    for file in os.listdir(zippath):
        f = zipfile.ZipFile(file+'.zip', 'w', zipfile.ZIP_DEFLATED)
        filepath = os.path.join(zippath,file)
        for file1 in os.listdir(filepath):
            filename = os.path.join(filepath,file1)
            print(filename)
            f.write(filename)
        f.close()

zipfun(rootpath)