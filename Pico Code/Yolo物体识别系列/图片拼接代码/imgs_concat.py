import cv2
import os

file_num1 = 64

for j in range(1, file_num1):

    path0 = "E:\\LDW\\" + str(j)
    path6 = "E:\\LDW\\" + str(j) + "\\1"

    list = os.listdir(path6)
    file_num2 = len(list)

    path3_1 = "E:\\LDW\\" + str(j) + "\\3\\-1.jpg"

    for i in range(0, file_num2):

        path1 = "E:\\LDW\\" + str(j) + "\\1\\" + str(i) + ".jpg"
        path2 = "E:\\LDW\\" + str(j) + "\\2\\" + str(i) + ".jpg"
        path3 = "E:\\LDW\\" + str(j) + "\\3\\" + str(i) + ".jpg"
        path4 = "E:\\LDW\\" + str(j) + "\\4\\" + str(i) + ".jpg"
        path5 = "E:\\LDW\\" + str(j) + "\\5\\" + str(i) + ".jpg"

        im1 = cv2.imread(path1)
        im2 = cv2.imread(path2)
        im3 = cv2.imread(path3)
        im4 = cv2.imread(path4)

        if im3 is None:
            im3 = cv2.imread(path3_1)

        A = cv2.vconcat((im1, im2))
        B = cv2.vconcat((im3, im4))
        C = cv2.vconcat((A, B))

        if os.path.isfile(path3):

            os.remove(path3)
        os.remove(path1)
        os.remove(path2)
        os.remove(path4)
        cv2.imwrite(path5, C)