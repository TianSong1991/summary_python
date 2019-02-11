# -*- coding:utf-8 -*-
# Author:Kevin Song
# Date:20181122
# 视频转图片

import cv2
cap = cv2.VideoCapture('F:\\UTool-DCAM700\\Save\\Video\\negative\\depth\\2018_11_22\\11_20_06.avi')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps =cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
i=0
while(cap.isOpened()):
    i=i+1
    ret, frame = cap.read()
    if ret==True:
        cv2.imwrite('I:\\test\\'+str(i)+'.png',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()

cv2.destroyAllWindows()