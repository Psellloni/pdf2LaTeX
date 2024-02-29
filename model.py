import cv2
from PIL import Image
from pix2tex.cli import LatexOCR
import pytesseract
import easyocr
import numpy as np
import os




def getTex(path, coord1, coord2, coord3, coord4):
    img = Image.open(path)
    img2 = img.crop((coord1[0], coord2[1] - 2 , coord3[0] + 3, coord3[1] - 3))
    # img2.show()
    model = LatexOCR()
    return str(model(img2))





def process_image(path):
    textBuffer = ''


    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    viz_img = np.copy(img)
    reader = easyocr.Reader(['en'])
    text_data = reader.readtext(img, width_ths=50, x_ths=4, height_ths=30, min_size=60, add_margin=0.2)  

    for data in text_data:
        print(data)
        # box, text
        box, text, conf= data
        top_left, top_right, bottom_right, bottom_left = box

        tl = [int(x) for x in top_left]
        br = [int(x) for x in bottom_right]
        cv2.rectangle(viz_img, tl, br, (0, 255, 0), 4)





    cv2.imwrite('viz_with_text8.jpg', viz_img)
    for block in text_data:
        print(block)
        if block[-1] > 0.5:
            textBuffer += "\\text{ " + block[-2] + " }"
        else:    
            textBuffer += getTex(path, block[0][0], block[0][1], block[0][2], block[0][3])
        


    return textBuffer



print(process_image("test3.jpg"))
