import cv2
import numpy as np
from PIL import Image
from pix2tex.cli import LatexOCR

def crop_x(sp, fp, matrix, img):
    model = LatexOCR()
    ans = ''
    for row in matrix[sp: fp + 1]:
        print(''.join(list(map(str, row[:200]))), '\n')

    x_vector = []

    for i in range(len(matrix[0])):
        sum = 0

        for j in range(sp, fp + 1):
            sum += matrix[j][i]
        
        if sum == 0:
            x_vector.append(0)
        
        else:
            x_vector.append(1)
    print(''.join(list(map(str, x_vector[:200]))))

    print('\n')
    print('\n')
    
    flag = True
    c = 0

    for i in range(len(x_vector)):
        if (x_vector[i] == 0) and flag:
            c += 1
        
        elif (x_vector[i] == 1) and flag and c >= 6:
            c = 0
            sp_x = i
            flag = False
        
        elif (x_vector[i] == 0) and (not flag) and c < 6:
            c += 1

        elif (x_vector[i] == 1) and (not flag) and c < 6:
            c = 0

        elif (x_vector[i] == 0) and (not flag) and c >= 6:
            c = 6
            flag = True
            fp_x = i - c

            img2 = img.crop((sp, fp, sp_x, fp_x))
            try:
                ans += (str(model(img2)) + ' ')
            except:
                ans += ' '
    
    print(ans)
            
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
            crop_x(sp, i, matrix, img)
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

preprocessing('test2.jpg')