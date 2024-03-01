import cv2
import numpy as np
from PIL import Image
import easyocr
import time

def crop_x(sp, fp, matrix):
    img = Image.open('test3.jpg')
    reader = easyocr.Reader(['en'])
    ans = ''

    x_vector = []
    indent = 20

    for i in range(len(matrix[0])):
        sum = 0

        for j in range(sp, fp + 1):
            sum += matrix[j][i]
        
        if sum == 0:
            x_vector.append(0)
        
        else:
            x_vector.append(1)
  
    flag = True
    c = 0
    counter2 = 1

    for i in range(len(x_vector)):
        if (x_vector[i] == 0) and flag:
            c += 1
        
        elif (x_vector[i] == 1) and flag and c >= indent:
            c = 0
            sp_x = i
            flag = False
        
        elif (x_vector[i] == 0) and (not flag) and c < indent:
            c += 1

        elif (x_vector[i] == 1) and (not flag) and c < indent:
            c = 0

        elif (x_vector[i] == 0) and (not flag) and c >= indent:
            c = indent
            flag = True
            fp_x = i - c

            img2 = img.crop((sp_x, sp, fp_x, fp))
            img2.show()
            time.sleep(2)

            counter2 += 1

            
def crop_y(matrix, img):
    y_vector = []

    for m in matrix:
        if sum(m) == 0:
            y_vector.append(0)

        else:
            y_vector.append(1)

    flag = True
    
    for i in range(len(y_vector)):
        if (y_vector[i] == 1) and (flag):
            sp = i - 1
            flag = False

        elif (y_vector[i] == 0) and (not flag):
            crop_x(sp, i, matrix)
            flag = True


def preprocessing(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    matrix = []

    for index in range(len(img)):
        row = []

        for index2 in range(len(img[index])):
            if sum(img[index][index2]) > 600:
                row.append(0)
            else:
                row.append(1)
        matrix.append(row)
    
    crop_y(matrix, img)

preprocessing('test3.jpg')