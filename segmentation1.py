import cv2
import numpy as np
from model2 import process_image
from model2 import getTex
from PIL import Image
import time


''' output for test3.jpg: {\mathcal{Z}}.\mathrm{Consider~a~function~}f(x);
f(x):\sum_{k=1}^{\infty}\left(x+{\frac{1}{n}}\right)^{n}
\left(\mathbf{a}\right)(0.5{\mathrm{~points}}){\mathrm{Define~domain~of~}}f(x)
\mathbf{\tau}(\mathbf{b})(1.5\ \mathrm{points}){\mathrm{Study~its~continuit}})
\mathrm{Hint}\colon\mathbf{a})\mathbf{f_{\mathrm{or}}}\mathrm{whien}\mathrm{{raines}}\mathrm{Of}\scriptstyle{\mathcal{X}}\operatorname{serics}\scriptstyle{\mathrm{onverges}}\mathbf{b})\scriptstyle{\mathrm{coninuily}}{\mathfrak{q}}:\mathrm{series}.\mathrm{Secec}{\mathrm{problem}}\mathbf{\nabla}2\operatorname{reon}
\mathrm{seminar}'''

'''output for test4.jpg: \pm\lambda{\frac{2}{x^{3}}}-{\frac{3}{x}};{\mathfrak{h}}{\mathfrak{h}}6x^{2}-4x+3z'''
counter2 = 1

def crop_x(sp, fp, matrix, img_cv, source):
    global counter2
    '''this function makes projection of segments we got from crop_y
    fuction and devide it into smaller segments using x-axis'''
    img_pil = Image.open(source)
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
    ans = ''
    i = 0

    while i != len(x_vector):
        if (x_vector[i] == 1) and flag:
            sp_x = i
            flag = False
        
        elif (x_vector[i] == 0) and (not flag) and c < indent:
            c += 1

        elif (x_vector[i] == 1) and (not flag) and c < indent:
            c = 0

        elif (not flag) and c >= indent:
            i -= c
            flag = True
            fp_x = i - c
            c = 0

            img_cv2 = img_cv[sp:(fp + 6), sp_x:(fp_x + 6)]
            img_pil2 = img_pil.crop((sp_x, sp, (fp_x + 6), (fp + 6)))
            '''img_pil2.show()
            time.sleep(2)'''
            cv2.imwrite(f'output2/seg{counter2}.jpg', img_cv2)

            '''here we send smallest segments to character recognition, works goofy'''
            counter2 += 1
            ans += getTex(img_pil2)
        i += 1

    return ans

            
def crop_y(matrix, img, source):
    '''this function makes a projection of data on y axis. This allow to segment 
    matrix by horizontal lines and then each segment goes to function crop_x'''
    y_vector = []

    result = ''

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
            result += crop_x(sp, i, matrix, img, source)
            flag = True
    
    return result



def preprocessing(source):
    '''this function transforms image into matrix of zeros and ones'''

    img = cv2.imread(source)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    matrix = []


    for index in range(len(img)):
        row = []

        for index2 in range(len(img[index])):
            '''here i count the sum of RGB and if it's higher than 600 (closer to white),
            I assume that it is white = 0'''
            if sum(img[index][index2]) > 600:
                row.append(0)

            else:
                row.append(1)

        matrix.append(row)
    
    return crop_y(matrix, img, source)