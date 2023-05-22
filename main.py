import torch
import argparse
import depthai as dai
from camera import Camera
from model import CustomModel
from state import State
from fileWriter import FileWriter
from utils.general import strip_optimizer
import cv2

@torch.no_grad()
def run(poseweights="yolov7-w6-pose.pt",device='cpu', show_output=False):

    camera = Camera()
    model = CustomModel(device, poseweights)
    fileW = FileWriter("coucou")
    state = State()

    # Connect to device and start pipeline
    with dai.Device(camera.pipeline) as deviceCamera:
         
        # Print camera information
        camera.printInformation(deviceCamera)

        # Output queue will be used to get the rgb frames from the output defined above
        qRgb = deviceCamera.getOutputQueue(name="rgb", maxSize=4, blocking=False)

        while True:
            inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived

            orig_image = inRgb.getCvFrame() 
            
            results = model.predict(orig_image) # Prediction and return a list of dict with all information

            state.findHandSign(results)
            state.findCurrentBBox(results)

            if state.isTracking():
                val1, val2 = state.calc()
                fileW.writeFile([val1, val2])

            state.prepareToNextFrame()
            
            if (show_output):
                radius = 5
                for elt in results:
                    cv2.circle(orig_image, (int(elt["x_rs"]), int(elt["y_rs"])), radius, (0, 0, 255), -1)
                    cv2.circle(orig_image, (int(elt["x_ls"]), int(elt["y_ls"])), radius, (0, 0, 255), -1)
                    cv2.circle(orig_image, (int(elt["x_rh"]), int(elt["y_rh"])), radius, (0, 0, 255), -1)
                    cv2.circle(orig_image, (int(elt["x_lh"]), int(elt["y_lh"])), radius, (0, 0, 255), -1)
                
                if state.lastBoundingBox != None:
                    cv2.rectangle(orig_image, state.lastBoundingBox[0:2], state.lastBoundingBox[2:4], (0, 255, 0), 2)
                
                cv2.imshow("Render", orig_image)
                k = cv2.waitKey(33)
                if k==27: return # Esc key to stop

                print(state.lastBoundingBox)
            

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--poseweights', nargs='+', type=str, default='weights/yolov7-w6-pose.pt', help='model path(s)')
    parser.add_argument('--device', type=str, default='cpu', help='cpu/0,1,2,3(gpu)')   #device arugments
    parser.add_argument('--show_output', action=argparse.BooleanOptionalAction)
    opt = parser.parse_args()
    return opt


#main function
def main(opt):
    run(**vars(opt))

if __name__ == "__main__":
    opt = parse_opt()
    strip_optimizer(opt.device,opt.poseweights)
    main(opt)