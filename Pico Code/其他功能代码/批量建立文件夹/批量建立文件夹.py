# Date:20180906
# Author:Tian Song

import os
root_path = 'I:\\人脸识别项目\\age_1\\1Kevin'
os.chdir(root_path)
for i in range(33,41):
    new_path = os.path.join(root_path,'error'+str(i))
    os.mkdir(new_path)