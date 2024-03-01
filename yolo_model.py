from ultralytics import FastSAM
from ultralytics.models.fastsam import FastSAMPrompt

from segmentation1 import preprocessing

def fs(source):
    model = FastSAM('FastSAM-s.pt')

    everything_results = model(source, device='cpu', retina_masks=True, imgsz=1024, conf=0.4, iou=0.9)

    prompt_process = FastSAMPrompt(source, everything_results, device='cpu')

    ann = prompt_process.everything_prompt()
    prompt_process.plot(annotations=ann, output='./output')

matrix = preprocessing('test2.jpg')

fs(matrix)