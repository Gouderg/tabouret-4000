import torch
import torch.onnx
from utils.torch_utils import select_device
from models.experimental import attempt_load
import blobconverter

# Transform .pt to .onnx model.

# model_dict = torch.load("weights/yolov7-w6-pose.pt")
# model = model_dict['model']
# model.eval()
# dummy_input = torch.randn(1, 3, 640, 640)
# torch.onnx.export(model, dummy_input, "weights/yolov7-w6-pose2.onnx", opset_version=11)

# Transforn .onnx to 


from blobconverter import BlobConverter

# Convert the ONNX model to TensorFlow SavedModel using BlobConverter
bc = BlobConverter()
bc.from_onnx('weights/yolov7-w6-pose2.onnx')
bc.to_tensorflow('weights/')