from ultralytics import FastSAM
from ultralytics.models.fastsam import FastSAMPrompt
from ultralytics import YOLO
from ultralytics import SAM
from ultralytics.data.annotator import auto_annotate

source = 'test2.jpg'

auto_annotate(data=source, det_model="yolov8x.pt", sam_model='sam_b.pt', device='cpu', output_dir='./output')

def FastSAM(source):
    model = FastSAM('FastSAM-s.pt')

    everything_results = model(source, device='cpu', retina_masks=True, imgsz=1024, conf=0.4, iou=0.9)

    prompt_process = FastSAMPrompt(source, everything_results, device='cpu')

    ann = prompt_process.everything_prompt()
    prompt_process.plot(annotations=ann, output='./output')


def sam_b(source):
    model = SAM('sam_b.pt')

    res = model(source)

    prompt_process = SAMPrompt(source, res, device='cpu')

    ann = prompt_process.everything_prompt()
    prompt_process.plot(annotations=ann, output='./output')
