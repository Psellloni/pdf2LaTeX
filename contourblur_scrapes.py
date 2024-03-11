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


# In[20]:


from collections import deque


# In[3]:


def contour(image_path, tres=(235, 300), show=False):
    img = cv2.imread(image_path,  cv2.IMREAD_GRAYSCALE)
    img = cv2.Canny(img, threshold1=tres[0], threshold2=tres[1])
    
    if show is True:
        plt.imshow(img, cmap='gray')
    
    return img


# In[4]:


def add_precision(vector, precision=1):
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


# In[5]:


img = 'test.jpg'


# In[6]:


def blur(img, precision=1, show=False):
    for row in img:
        add_precision(row, precision)
    if show is True:
        plt.imshow(img, cmap='gray')
    return img


# In[7]:


image = cv2.imread(img,  cv2.IMREAD_GRAYSCALE)


# In[8]:


plt.imshow(image, cmap='gray')


# In[31]:


cont_img = contour(img, tres=(375, 451), show=True)


# In[51]:


blurred = blur(cont_img, precision=39, show=True)


# In[52]:


blurred[blurred != 0] = 1 


# In[53]:


blurred


# In[54]:


image = cv2.imread(img,  cv2.IMREAD_GRAYSCALE)


# In[55]:


# plt.imshow(image[blurred], cmap='gray')


# In[56]:


iz = np.where(blurred.astype(bool), image, 255)


# In[57]:


plt.imshow(iz, cmap='gray')


# In[58]:


been = np.zeros_like(blurred)


# In[59]:


# [i][j+-1]
# [i+-1][j]


# In[60]:


def BFS_element(blurred, been, coords, show=False):
    
    element = np.zeros_like(blurred)
    element[coords[0]][coords[1]] = 1
    
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
            element[i][j - 1] = 1
        
        if (i - 1 >= 0) and (been[i - 1][j] == 0) and (blurred[i - 1][j] == 1):
            q_x.append(j)
            q_y.append(i - 1)

            been[i - 1][j] = 1
            element[i - 1][j] = 1
        
        if (j + 1 < len(blurred[0])) and (been[i][j + 1] == 0) and (blurred[i][j + 1] == 1):
            q_x.append(j + 1)
            q_y.append(i)

            been[i][j + 1] = 1
            element[i][j + 1] = 1
        
        if (i + 1 < len(blurred)) and (been[i + 1][j] == 0) and (blurred[i + 1][j] == 1):
            q_x.append(j)
            q_y.append(i + 1)

            been[i + 1][j] = 1
            element[i + 1][j] = 1
        
    if show is True:
        plt.imshow(element, cmap='gray')
        
    return element


# In[62]:


been = np.zeros_like(blurred)
elements = []
while not np.array_equal(been, blurred):
    for i in range(len(blurred)):
        for j in range(len(blurred[i])):
            if (blurred[i][j] != 0) and (been[i][j] == 0):
                been[i][j] = 1
                element = BFS_element(blurred, been, coords=(i, j), show=False)
                elements.append(element)


# In[63]:


for element in elements:
    plt.imshow(element, cmap='gray')


# In[68]:


plt.imshow(elements[2], cmap='gray')


# In[73]:


def show_part_of_image(element, image):
    el_mask = element
    el_mask[el_mask != 0] = 1
    el_mask = el_mask.astype(bool)
    
    iz = np.where(el_mask.astype(bool), image, 0)
    
    plt.imshow(iz, cmap='gray')


# In[82]:


show_part_of_image(elements[12], image)


# In[ ]:




