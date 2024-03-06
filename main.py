from segmentation import ImageSegmentationModel

source = 'tests/test1.png'

model = ImageSegmentationModel()
model.fit(source, indent_x=10, output_dir='output/')