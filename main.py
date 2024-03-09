from segmentation import ImageSegmentationModel

source = 'tests/test1.png'

model = ImageSegmentationModel()
prediction = model.predict(source, indent_y=4, indent_x=15,  output_dir='output/')

print(prediction)
