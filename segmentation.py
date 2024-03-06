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
    counter_x = 1
    counter_y = 1

    # write crop x using np matrix and make it recursive
    def crop_x(self, matrix, img_cv):

        img_pil = Image.open(self.source)

        self.cropped_x = False

        flag = True
        crop_counter = 0
        output = ''
        counter = 0
        index = 0

        sums = np.sum(matrix, axis = 0)
        x_vector = [int(bool(v)) for v in sums]
        x_vector = np.array(x_vector)

        while index < len(x_vector):
            if (x_vector[index]) and (flag):
                start_pointer_x = index
                flag = False

            elif (not flag) and (counter >= self.indent_x):
                flag = True
                counter = 0
                #img_pil2 = img_pil.crop((start_pointer_x, start_pointer_y, (end_pointer_x + 20), end_pointer_y))
                cv2.imwrite(('output_x/' + f'seg{self.counter_x}.jpg'), img_cv[:, start_pointer_x:index])
                crop_counter += 1
                self.counter_x += 1
                index -= counter
                self.cropped_x = True
                #output += process_image(img_pil2, img_cv2)

                if not crop_counter > 2:
                    self.crop_y(matrix[:, start_pointer_x:index], img_cv[:, start_pointer_x:index])

                        
            elif (not x_vector[index]) and (not flag):
                counter += 1
            
            elif (x_vector[index]) and (not flag):
                counter = 0

            index += 1

        '''if (not flag):

            img_cv2 = img_cv[:, start_pointer_x:(index - counter)]
            #img_pil2 = img_pil.crop((start_pointer_x, start_pointer_y, (end_pointer_x - 1), end_pointer_y))

            cv2.imwrite(('output_x/' + f'seg{self.counter2}.jpg'), img_cv2)

            if crop_counter:
                self.crop_y(matrix[:, start_pointer_x:(index - counter)], img_cv[:, start_pointer_x:(index - counter)])

            self.counter2 += 1

            #output += process_image(img_pil2, img_cv2)'''



        return None


    def crop_y(self, matrix, img):
        '''this function makes a projection of data on y axis. This allow to segment 
        matrix by horizontal lines and then each segment goes to function crop_x'''
        y_vector = []

        result = ''

        self.cropped_y = False

        # projection on y axis
        for i in range(len(matrix)):
            if np.sum(matrix[i]):
                y_vector.append(1)

            else:
                y_vector.append(0)

        y_vector = np.array(y_vector)
        flag = True
        counter2 = 1
        counter3 = 0
        crop_counter = 0
        index = 0
        
        while index != len(y_vector):
            if (y_vector[index]) and (flag):
                start_pointer_y = index
                flag = False

            elif (not y_vector[index]) and (not flag) and (counter3 >= self.indent_y or (not crop_counter)):
                cv2.imwrite(f'output_y/seg{self.counter_y}.jpg', img[start_pointer_y:(index + 1), :])

                self.counter_y += 1

                self.cropped_y = True

                self.crop_x(matrix[start_pointer_y:(index + 1)], img[start_pointer_y:(index + 1)])

                if not crop_counter:
                    self.crop_x(matrix, img)

                crop_counter += 1
                index -= counter3
                counter3 = 0
                flag = True

            elif (not y_vector[index]) and (not flag):
                counter3 += 1

            elif (y_vector[index]) and (not flag):
                counter3 = 0

            index += 1
        
        return None


    def preprocessing(self, source, indent_x=20, indent_y=2, output_dir='output/', *args, **kwargs):
        '''this function transforms image into matrix of zeros and ones'''

        print('это нахуй не нужно', args)
        print('это тоже', kwargs)

        self.source = source
        self.indent_x = indent_x
        self.indent_y = indent_y
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


class ImageSegmentationModel:

    def __init__(self):

        pass


    def fit(self, source, indent_x=40, indent_y=2, output_dir='output/', *args, **kwargs):

        self.source = source
        self.indent_x = indent_x
        self.indent_y = indent_y
        self.output_dir = output_dir
        self.seg_index = 1
        self.cropped = True

        image = self.read_image(source)

        matrix = self.create_bin_matrix(image)

        self.crop(matrix, image, axis=0)

    

    def read_image(self, source):

        image = cv2.imread(self.source)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        return image
    

    def create_bin_matrix(self, image):

        matrix = []

        for index in range(len(image)):

            row = []

            for index2 in range(len(image[index])):
                '''here i count the sum of RGB and if it's higher than 600 (closer to white),
                I assume that it is white = 0'''

                if sum(image[index][index2]) > 600:
                    row.append(0)

                else:
                    row.append(1)

            matrix.append(row)
        
        return np.array(matrix)
    

    def crop(self, matrix, image, axis):

        bin_vector = self.create_vector(matrix, axis=axis)

        print(bin_vector)

        if axis:

            req_indent = self.indent_x

        else:

            req_indent = self.indent_y

        index = 0
        curr_indent = 0
        flag_segment = False
        flag_cropped = False

        while index != len(bin_vector):

            if (bin_vector[index]) and (not flag_segment):

                start_pointer = index
                flag_segment = True

            elif (not bin_vector[index]) and (flag_segment) and (curr_indent < req_indent):

                curr_indent += 1

            elif (not bin_vector[index]) and (flag_segment) and (curr_indent >= req_indent):

                if axis:

                    cv2.imwrite(self.output_dir + f'seg{self.seg_index}.jpg', image[start_pointer: index])

                    self.seg_index += 1

                    self.crop(matrix[start_pointer: index], image[start_pointer: index], axis=int(not axis))
                
                else:

                    cv2.imwrite(self.output_dir + f'seg{self.seg_index}.jpg', image[:, start_pointer: index])

                    self.seg_index += 1

                    self.crop(matrix[:, start_pointer: index], image[:, start_pointer: index], axis=int(not axis))

                index -= (curr_indent + 1)
                curr_indent = 0
                flag_segment = False
                flag_cropped = True

            elif (bin_vector[index]) and (flag_segment):
                curr_indent = 0

            index += 1

        if (self.cropped) or (flag_cropped):

            self.cropped = flag_cropped

            cv2.imwrite(self.output_dir + f'seg{self.seg_index}.jpg', image)

            self.seg_index += 1

            self.crop(matrix, image, axis=int(not axis))

    
    def create_vector(self, matrix, axis):

        vector_of_sums = np.sum(matrix, axis=int(not axis))

        bin_vector =  [int(bool(v)) for v in vector_of_sums]

        return np.array(bin_vector)