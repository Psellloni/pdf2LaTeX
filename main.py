from segmentation import Segmentation

source = 'tests/test3.jpg'

seg = Segmentation()
print(seg.preprocessing(source, indent=30, output_dir='output/'))