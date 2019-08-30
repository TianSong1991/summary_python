import os
import cv2
import numpy as np

def show_IR_img(IR_path1,IR_path):
    def contrast_brightness_image(src1, a, g):
        h, w, ch = src1.shape
        src2 = np.zeros([h, w, ch], src1.dtype)
        dst = cv2.addWeighted(src1, a, src2, 1 - a, g)
        return dst
    i = 1
    for file in os.listdir(IR_path1):
        path1 = os.path.join(IR_path1, file)

        img16 = cv2.imread(path1, cv2.IMREAD_ANYDEPTH)

        img8 = img16.reshape(480, 640, 1)

        img = contrast_brightness_image(img8, 20, 50)
        cv2.imwrite(os.path.join(IR_path, str(i).zfill(5) + ".png"), img)
        i = i + 1

def tran_img2avi(IR_path1,IR_path):
    fps = 24
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    video_writer = cv2.VideoWriter(filename=os.path.join(IR_path1,'result.avi'), fourcc=fourcc, fps=fps, frameSize=(640, 480))

    for file1 in os.listdir(IR_path):
        path2 = os.path.join(IR_path,file1)
        img = cv2.imread(path2)
        cv2.waitKey(100)
        video_writer.write(img)
        print(file1)
    video_writer.release()


if __name__ == '__main__':
    IR_path1 = 'H:\\CV2\\data\\15\\ir'
    path,ir = os.path.split(IR_path1)
    IR_path = os.path.join(path,'gray')
    if not os.path.exists(IR_path):
        os.makedirs(IR_path)
    show_IR_img(IR_path1, IR_path)
    tran_img2avi(IR_path1, IR_path)