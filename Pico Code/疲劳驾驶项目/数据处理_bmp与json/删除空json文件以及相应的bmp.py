import os
import json
import shutil

root_path = 'E:\\Project_FDS\\data_1030\\4mouth_smoke\\4mouth_smoke\\picture\\part2'

os.chdir(root_path)
all_files = os.listdir(root_path)

for file1 in all_files:
    path1 = os.path.join(root_path,file1)
    files1 = os.listdir(path1)
    for file2 in files1:
        (name1,extension1) = os.path.splitext(file2)
        path2 = os.path.join(path1,file2)
        path2_1 = os.path.join(path1,name1)
        if extension1 == '.json':          
            json_file = open(path2,'r')
            json_file_1 = json_file.read()
            json_file.close()
            json_file_2 = json.JSONDecoder().decode(json_file_1)
            if len(json_file_2["faces"]) == 0:

                print(path2,path2_1)
                os.remove(path2)
                os.remove(path2_1)

print("Done!")