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

class Segmentation:
    counter2 = 1

    # write crop x using np matrix and make it recursive
    def crop_x(self, matrix, img_cv):

        img_pil = Image.open(self.source)

        flag = True
        output = ''
        counter = 0
        index = 0

        sums = np.sum(matrix, axis = 0)
        x_vector = [int(bool(v)) for v in sums]
        x_vector = np.array(x_vector)

        while index < len(x_vector):
            if (x_vector[index] == 1) and flag:
                start_pointer_x = index
                flag = False
            
            elif (not x_vector[index]) and (not flag) and (counter < self.indent):
                counter += 1

            elif (x_vector[index]) and (not flag) and (counter < self.indent):
                counter = 0

            elif (not flag) and (counter >= self.indent):
                index -= counter
                flag = True
                counter = 0

                img_cv2 = img_cv[:, start_pointer_x:index]
                #img_pil2 = img_pil.crop((start_pointer_x, start_pointer_y, (end_pointer_x + 20), end_pointer_y))
                cv2.imwrite(('output_x/' + f'seg{self.counter2}.jpg'), img_cv2)
                self.counter2 += 1
                #output += process_image(img_pil2, img_cv2)

            index += 1

        if (not flag):
            end_pointer_x = index - counter

            img_cv2 = img_cv[:, start_pointer_x:(end_pointer_x - 1)]
            #img_pil2 = img_pil.crop((start_pointer_x, start_pointer_y, (end_pointer_x - 1), end_pointer_y))

            cv2.imwrite(('output_x/' + f'seg{self.counter2}.jpg'), img_cv2)

            self.counter2 += 1

            #output += process_image(img_pil2, img_cv2)


        return output


    '''def crop_x_prime(matrix):
        x_vector_prime = []

        for i in range(len(matrix[0])):
            sum = 0

            for j in range(len(matrix)):
                sum += matrix[j][i]

            if sum == 0:
                x_vector_prime.append(0)
            
            else:
                x_vector_prime.append(1)
        
        flag_cuted = False
        flag = True

        for i in range(len(x_vector_prime)):
            if (x_vector_prime[i]) and flag:
                start_pointer_x_prime = i
                flag = True
                flag_cuted = False

            if (not x_vector_prime[i]) and (not flag):
                crop_y'''


    def crop_y(self, matrix, img):
        '''this function makes a projection of data on y axis. This allow to segment 
        matrix by horizontal lines and then each segment goes to function crop_x'''
        y_vector = []

        result = ''

        for i in range(len(matrix)):
            if np.sum(matrix[i]):
                y_vector.append(1)

            else:
                y_vector.append(0)

        y_vector = np.array(y_vector)
        flag = True
        counter2 = 1
        
        for index in range(len(y_vector)):
            if (y_vector[index]) and (flag):
                start_pointer_y = index - 1
                flag = False

            elif (not y_vector[index]) and (not flag):
                cv2.imwrite(f'output_y/seg{counter2}.jpg', img[start_pointer_y:(index + 1), :])

                counter2 += 1

                result += self.crop_x(matrix[start_pointer_y:(index + 1)], img[start_pointer_y:(index + 1)])
                flag = True

        
        return result


    def preprocessing(self, source, indent=30, output_dir='output/'):
        '''this function transforms image into matrix of zeros and ones'''
        self.source = source
        self.indent = indent
        self.output_dir = output_dir

        img = cv2.imread(self.source)
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
        
        matrix2 = np.array(matrix)
        
        return self.crop_y(matrix2, img)