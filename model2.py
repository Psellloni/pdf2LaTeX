from PIL import Image
from pix2tex.cli import LatexOCR
import easyocr
import numpy as np
import os


def getTex(img):
    model = LatexOCR()
    return str(model(img))


def process_image(img_pil=None, img_cv=None):
    textBuffer = ''
    reader = easyocr.Reader(['ru'])
    text_data = reader.readtext(img_cv)  

    print(text_data)

    '''for block in text_data:
        print(block)
        if block[-1] > 0.65:
            textBuffer += "\\text{ " + block[-2] + " }"
        else:    
            textBuffer += getTex(img_pil)'''
        


    # return textBuffer



#print(process_image("test2.jpg"))
