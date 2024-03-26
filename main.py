from BFS_segmentation_class import Segmentation_BFS
from model2 import process_image
import cv2

segmentation = Segmentation_BFS()

segments = segmentation.get_segments('tests/test3.jpg')

for seg in segments:

    seg = segmentation.cut_picture(seg)

    cv2.imshow('image', seg)
    cv2.waitKey(0)