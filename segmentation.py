import cv2
import numpy as np
from model2 import process_image
from model2 import getTex
from PIL import Image


''' output for test3.jpg: {\mathcal{Z}}.\mathrm{Consider~a~function~}f(x);
f(x):\sum_{k=1}^{\infty}\left(x+{\frac{1}{n}}\right)^{n}
\left(\mathbf{a}\right)(0.5{\mathrm{~points}}){\mathrm{Define~domain~of~}}f(x)
\mathbf{\tau}(\mathbf{b})(1.5\ \mathrm{points}){\mathrm{Study~its~continuit}})
\mathrm{Hint}\colon\mathbf{a})\mathbf{f_{\mathrm{or}}}\mathrm{whien}\mathrm{{raines}}\mathrm{Of}\scriptstyle{\mathcal{X}}\operatorname{serics}\scriptstyle{\mathrm{onverges}}\mathbf{b})\scriptstyle{\mathrm{coninuily}}{\mathfrak{q}}:\mathrm{series}.\mathrm{Secec}{\mathrm{problem}}\mathbf{\nabla}2\operatorname{reon}
\mathrm{seminar}'''

'''output for test4.jpg: \pm\lambda{\frac{2}{x^{3}}}-{\frac{3}{x}};{\mathfrak{h}}{\mathfrak{h}}6x^{2}-4x+3z'''
counter2 = 1

def crop_x(start_pointer_y, end_pointer_y, matrix, img_cv, source, indent, output_dir):
    global counter2
    '''this function makes projection of segments we got from crop_y
    fuction and devide it into smaller segments using x-axis'''


    img_pil = Image.open(source)
    x_vector = []
    flag = True
    output = ''
    counter = 0
    index = 0

    '''This loop create a projection of matrix on axis x'''
    for i in range(len(matrix[0])):
        sum = 0

        for j in range(start_pointer_y, end_pointer_y + 1):
            sum += matrix[j][i]
        
        if sum == 0:
            x_vector.append(0)
        
        else:
            x_vector.append(1)


    while index < len(x_vector):
        if (x_vector[index] == 1) and flag:
            start_pointer_x = index
            flag = False
        
        elif (not x_vector[index]) and (not flag) and (counter < indent):
            counter += 1

        elif (x_vector[index]) and (not flag) and (counter < indent):
            counter = 0

        elif (not flag) and (counter >= indent):
            index -= counter
            flag = True
            end_pointer_x = index - counter
            counter = 0

            img_cv2 = img_cv[start_pointer_y:end_pointer_y, start_pointer_x:(end_pointer_x + 60)]
            img_pil2 = img_pil.crop((start_pointer_x, start_pointer_y, (end_pointer_x + 60), end_pointer_y))

            '''this part save our segments in a folder'''
            cv2.imwrite((output_dir + f'seg{counter2}.jpg'), img_cv2)

            '''here we send smallest segments to character recognition, works goofy'''
            counter2 += 1
            output += getTex(img_pil2)

        index += 1

    if (not flag):
        end_pointer_x = index - counter

        img_cv2 = img_cv[start_pointer_y:end_pointer_y, start_pointer_x:(end_pointer_x - 1)]
        img_pil2 = img_pil.crop((start_pointer_x, start_pointer_y, (end_pointer_x - 1), end_pointer_y))

        cv2.imwrite((output_dir + f'seg{counter2}.jpg'), img_cv2)

        counter2 += 1

        '''here we send smallest segments to character recognition, works goofy'''
        output += getTex(img_pil2)


    return output

            
def crop_y(matrix, img, source, indent, output_dir):
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
    
    for index in range(len(y_vector)):
        if (y_vector[index]) and (flag):
            start_pointer_y = index - 1
            flag = False

        elif (not y_vector[index]) and (not flag):
            result += crop_x(start_pointer_y, index, matrix, img, source, indent, output_dir)
            flag = True
    
    return result



def preprocessing(source, indent=30, output_dir='output/'):
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
    
    return crop_y(matrix, img, source, indent, output_dir)