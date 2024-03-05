from segmentation import Segmentation

source = 'tests/test1.png'

seg = Segmentation()
print(seg.preprocessing(source, output_dir='output/'))