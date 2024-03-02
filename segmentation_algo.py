#!/usr/bin/env python
# coding: utf-8

# In[9]:


# !pip install easyocr


# In[10]:


import cv2
import numpy as np
from PIL import Image
import easyocr
import time


# In[11]:


from collections import deque


# In[12]:


# def radius_crop(matrix, precision=1):
#     remain = matrix
#     que = deque()
#     segments = [] #матрица сегментов
   
#     for i in range(len(remain[0])):
#         start = remain[i].find(1)
#         if start != -1:


# In[13]:


def add_precision(vector, precision):
    if (precision == 0):
        return vector
    
    i = 0
    fin = len(vector)
    
    while True:
        if (vector[i] == 1):
            if ((i != 0) and (vector[i - 1] == 0)):
                for j in range(max(0, i - precision), i):
                    vector[j] = 1
            if ((i != len(vector) - 1) and (vector[i + 1] == 0)):
                for j in range(i, min(len(vector), i + precision + 1)):
                    vector[j] = 1
                i = min(len(vector), i + precision + 1) - 1
                
                
        i += 1
        if i >= len(vector) - 1:
            break

    return vector


# In[20]:


def crop_x(sp, fp, np_matrix, precision):
    img = Image.open('formules_2221.png')
    reader = easyocr.Reader(['en'])
    ans = ''

#     x_vector = []

#     for i in range(len(matrix[0])):
#         sum = 0

#         for j in range(sp, fp + 1):
#             sum += matrix[j][i]
        
#         if sum == 0:
#             x_vector.append(0)
        
#         else:
#             x_vector.append(1)

    y_segment = np_matrix[sp:fp,:]
    
    x_vector = y_segment.sum(axis=0)
    x_vector[x_vector != 0] = 1
    
  
    flag = True
    c = 0

    x_vector = add_precision(x_vector, precision)
    
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

            img2 = img.crop((sp_x, sp, fp_x, fp))
            img2.show()
            time.sleep(2)


# In[17]:


def crop_y(np_matrix, img, precision):
    
    y_vector = np_matrix.sum(axis=1)
    y_vector[y_vector != 0] = 1

    flag = True
    
    y_vector = add_precision(y_vector, precision)
    
    for i in range(len(y_vector)):
        if (y_vector[i] == 1) and (flag):
            sp = i - 1
            flag = False

        elif (y_vector[i] == 0) and (not flag):
            crop_x(sp, i, np_matrix, precision)
            flag = True


# In[22]:


def preprocessing(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    matrix = []

    
    np_img = np.array(img)
    np_matrix = np.where(np_img.sum(axis=2) > 600, 0, 1)
    
#     matrix = list(np_matrix)
    
    precision = int(input())
    
    crop_y(np_matrix, img, precision)

preprocessing('formules_2221.png')


# In[ ]:





# In[ ]:




