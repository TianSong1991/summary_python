import matplotlib.pyplot as plt
import numpy as np
import cv2
import os

data_image_files = 'F:\\pic\\RGB'  # face_set
datatempimg = os.listdir(data_image_files)

for i in range(0, len(datatempimg)):
    img_dir = data_image_files + '/' + datatempimg[i]
    #print(img_dir)
    f = open(img_dir, mode='rb')
    x = np.fromfile(f, dtype=np.ubyte)
    x = x.reshape(1080, 1920, 3)
    '''n1 = int(1920/5)
    x = x[:, n1:n1*4 , :]'''
    write_dir = data_image_files.replace('rgb', 'write_dir')
    if os.path.exists(write_dir):
        cv2.imwrite(write_dir + '/' + datatempimg[i] + '.jpg', x)
    else:
        os.makedirs(write_dir)
        cv2.imwrite(write_dir + '/' + datatempimg[i] + '.jpg', x)

    # cv2.imshow('img', x)
    # cv2.waitKey(0)

    '''plt.imshow(x)
    plt.axis('off')  
    plt.show()'''
    f.close()
