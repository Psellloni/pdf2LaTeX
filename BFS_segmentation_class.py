#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PIL import Image
from pix2tex.cli import LatexOCR
import pytesseract
import easyocr
import numpy as np
import os
import matplotlib.pyplot as plt
import cv2
from collections import deque


# In[2]:


class Segmentation_BFS:
   def __init__(self):
       pass

   '''Cегментация'''

   #Ищет контур изображения
   def contour(self, image_path, tres=(235, 300), show=False):
       img = cv2.imread(image_path,  cv2.IMREAD_GRAYSCALE)
       img = cv2.Canny(img, threshold1=tres[0], threshold2=tres[1])

       if show is True:
           plt.imshow(img, cmap='gray')

       return img

   #Размазывает одну строку/cтолбец (вектор) на precision в обе стороны
   def add_precision(self, vector, precision=1):
       if (precision == 0):
           return vector

       i = 0
       fin = len(vector)

       while True:
           if (vector[i] != 0):
               if ((i != 0) and (vector[i - 1] == 0)):
                   for j in range(max(0, i - precision), i):
                       vector[j] = vector[i]
               if ((i != len(vector) - 1) and (vector[i + 1] == 0)):
                   for j in range(i, min(len(vector), i + precision + 1)):
                       vector[j] = vector[i]
                   i = min(len(vector), i + precision + 1) - 1


           i += 1
           if i >= len(vector) - 1:
               break

       return vector

   #Итеративно вызывает add_precision() для каждой строки (если ось х) 
   #или каждого столбца (если ось у), тем самым размазывая изображение
   def blur(img, precision=1, axis='x', show=False):

       t_img = img.copy()

       if axis != 'x':
           t_img = t_img.T

       for row in t_img:
           add_precision(row, precision)

       if axis != 'x':
           t_img = t_img.T

       if show is True:
           plt.imshow(t_img, cmap='gray')

       return t_img


   #Запускает обход в ширину при обнаружении размазни. Вызывается в следующей функции
   def BFS_segment(blurred, been, coords, show=False):

       segment = np.zeros_like(blurred)
       segment[coords[0]][coords[1]] = 1

       q_x = deque()
       q_x.append(coords[1])

       q_y = deque()
       q_y.append(coords[0])

       while q_x:
           i = q_y.popleft()
           j = q_x.popleft()

           if (j - 1 >= 0) and (been[i][j - 1] == 0) and (blurred[i][j - 1] == 1):
               q_x.append(j - 1)
               q_y.append(i)

               been[i][j - 1] = 1
               segment[i][j - 1] = 1

           if (i - 1 >= 0) and (been[i - 1][j] == 0) and (blurred[i - 1][j] == 1):
               q_x.append(j)
               q_y.append(i - 1)

               been[i - 1][j] = 1
               segment[i - 1][j] = 1

           if (j + 1 < len(blurred[0])) and (been[i][j + 1] == 0) and (blurred[i][j + 1] == 1):
               q_x.append(j + 1)
               q_y.append(i)

               been[i][j + 1] = 1
               segment[i][j + 1] = 1

           if (i + 1 < len(blurred)) and (been[i + 1][j] == 0) and (blurred[i + 1][j] == 1):
               q_x.append(j)
               q_y.append(i + 1)

               been[i + 1][j] = 1
               segment[i + 1][j] = 1

       if show is True:
           plt.imshow(segment, cmap='gray')

       return segment
       
   #Ищет размазни, встречая их вызывает обход в ширину (BFS_segment)
   def segmentation_BFS(blurred):
       been = np.zeros_like(blurred)
       blurred[blurred != 0] = 1
       segments = []
       while not np.array_equal(been, blurred):
           for i in range(len(blurred)):
               for j in range(len(blurred[i])):
                   if (blurred[i][j] != 0) and (been[i][j] == 0):
                       been[i][j] = 1
                       segment = BFS_segment(blurred, been, coords=(i, j), show=False)
                       segments.append(segment)
       return segments
       
       
   #Объединяет предыдущие функции для поиска сегментов
   def get_segments(image_path, cont_tres=(500, 600), precision=(6, 4)):
       image = cv2.imread(image_path,  cv2.IMREAD_GRAYSCALE)
       cont_img = contour(image_path, tres=cont_tres)
       blurred = blur(cont_img, precision=precision[0], axis='x')
       blurred = blur(blurred, precision=precision[1], axis='y')
       segments = segmentation_BFS(blurred)
       return segments
   
   
   '''Методы визуализации и получения изображения'''
   
   #Возвращает кусок изображения принадлежащий сегменту
   def show_part_of_image(segment, image, show=False):
       mask = segment.copy()
       mask[mask != 0] = 1
       mask = mask.astype(bool)

       iz = np.where(mask.astype(bool), image, 0)
       
       if show is True:
           plt.imshow(iz, cmap='gray')

       return iz
   
   #Возвращает квадрат сегмента и сегмент в нем (в виде маски)
   def cut_projection(segment, show=False):
       x_proj = segment.any(axis=0)
       y_proj = segment.any(axis=1)


       def find_first(proj):
           for i in range(len(proj)):
               if proj[i]!=0:
                   return i

       def find_last(proj):
           for i in range(len(proj) - 1, 0, -1):
               if proj[i]!=0:
                   return i

       y_first = find_first(y_proj)
       y_last = find_last(y_proj)
       x_first = find_first(x_proj)
       x_last = find_last(x_proj) 

       cut_segment = segment.copy()[y_first:y_last, x_first:x_last]

       cut_segment[cut_segment!=0] = 255

       if show is True:
           plt.imshow(cut_segment, cmap='gray')

       return cut_segment
   
   #Возвращает квадрат исходного изображения которому принадлежит сегмент
   def cut_picture(segment, image, show=False):
       x_proj = segment.any(axis=0)
       y_proj = segment.any(axis=1)


       def find_first(proj):
           for i in range(len(proj)):
               if proj[i]!=0:
                   return i

       def find_last(proj):
           for i in range(len(proj) - 1, 0, -1):
               if proj[i]!=0:
                   return i

       y_first = find_first(y_proj)
       y_last = find_last(y_proj)
       x_first = find_first(x_proj)
       x_last = find_last(x_proj) 

       cut_image = image.copy()[y_first:y_last, x_first:x_last]


       if show is True:
           plt.imshow(cut_image, cmap='gray')

       return cut_image

