import cv2
import numpy as np
from model2 import process_image
from model2 import getTex
from PIL import Image


class ImageSegmentationModel:

    def __init__(self):

        pass


    def predict(self, source, indent_x=40, indent_y=2, output_dir='output/', *args, **kwargs):
        ''' this method reads path to file from source and sets model features '''

        if args or kwargs:

            print('нахуя ты это написал: ', args, kwargs)

        self.source = source
        self.indent_x = indent_x
        self.indent_y = indent_y
        self.output_dir = output_dir
        self.seg_index = 1
        self.cropped = True
        self.output = ''

        image = self.read_image(source)

        matrix = self.create_bin_matrix(image)

        self.crop(matrix, image, axis=1)

        return self.output

    

    def read_image(self, source, *args, **kwargs):
        ''' this method reads image from png or jpg to a numpy array '''

        image = cv2.imread(self.source)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        return image
    

    def create_bin_matrix(self, image, *args, **kwargs):
        ''' this method creates a binary matrix of input image where 0 is white and 1 is black.
        We consider that if a sum of RGB variables is grater than 600 it's a white color'''

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
    

    def crop(self, matrix, image, axis, cropped=True, *args, **kwargs):
        ''' this is a recursiva method which cropes matrix and image by one of 2
        axises and colls itself with changing of axis to the opposite one'''

        # create a binary vector of projection of our matrix on axis we use
        bin_vector = self.create_vector(matrix, axis=axis)

        # set an intend based on axis we use
        if axis:

            req_indent = self.indent_x

        else:

            req_indent = self.indent_y

        index = 0
        curr_indent = 0
        flag_segment = False
        flag_cropped = False

        # this cycle goues through binary vector to find group of ones which we crop as an independant segment
        while index != len(bin_vector):

            # this block sets a starting point of our segment when we 
            # meet a first 1 and set flag_segment to True indicating 
            # that we start determining out segment length
            if (bin_vector[index]) and (not flag_segment):

                start_pointer = index
                flag_segment = True

            # this block countes the number of 0 when we determining the
            # segment length to compare it to our required indent
            elif (not bin_vector[index]) and (flag_segment) and (curr_indent < req_indent):

                curr_indent += 1

            # this block is used when algorithm finds zero and current 
            # indent equals or exceeds required one. When this happens 
            # algorithms considers given axis and calls recursivly itself 
            # using the segment as an argument and changing an axis to the 
            # opposite one.
            elif (not bin_vector[index]) and (flag_segment) and (curr_indent >= req_indent):

                if axis:

                    cv2.imwrite(self.output_dir + f'seg{self.seg_index}.jpg', image[:, start_pointer: index])

                    self.seg_index += 1

                    self.crop(matrix[:, start_pointer: index], image[:, start_pointer: index], axis=int(not axis))
                
                else:

                    cv2.imwrite(self.output_dir + f'seg{self.seg_index}.jpg', image[start_pointer: index])

                    self.seg_index += 1

                    self.crop(matrix[start_pointer: index], image[start_pointer: index], axis=int(not axis))

                index -= (curr_indent + 1)
                curr_indent = 0
                flag_segment = False
                flag_cropped = True

            # this block is used when flag_segment is True and we meet 1. 
            # If this happens then the precounted currend intend is set 
            # to 0 as it's not long enough to separate the segments
            elif (bin_vector[index]) and (flag_segment):
                curr_indent = 0

            index += 1

        # This block is used when the binary vector ends but the flag_segment 
        # is True meaning that algorithm didn't find the end of the segment. 
        # In this case algorithm considers that this segment ends when the matrix ends.
        if ((cropped) or (flag_cropped)) and (flag_segment):

            if axis:
                
                cv2.imwrite(self.output_dir + f'seg{self.seg_index}.jpg', image[:, start_pointer:])

                self.seg_index += 1

                self.crop(matrix[:, start_pointer:], image[:, start_pointer:], axis=int(not axis), cropped=flag_cropped)
            
            else:
                
                cv2.imwrite(self.output_dir + f'seg{self.seg_index}.jpg', image[start_pointer:])

                self.seg_index += 1

                self.crop(matrix[start_pointer:], image[start_pointer:], axis=int(not axis), cropped=flag_cropped)
        
        if (not cropped) and (not flag_cropped):

            self.output += process_image(image)

    
    def create_vector(self, matrix, axis, *args, **kwargs):
        ''' this method creates a binary vector of projection of the matrix on a required axis'''

        vector_of_sums = np.sum(matrix, axis=int(not axis))

        bin_vector =  [int(bool(v)) for v in vector_of_sums]

        return np.array(bin_vector)