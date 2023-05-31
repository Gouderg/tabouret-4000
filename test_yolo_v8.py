import ultralytics 
from ultralytics import YOLO

import torch
import argparse
import depthai as dai
from camera import Camera
from model import CustomModel
from state import State
from fileWriter import FileWriter
from utils.general import strip_optimizer
import cv2

# @torch.no_grad()
def run(poseweights, device, show_output=True):
    
    ultralytics.checks()
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
            
            results = model.predict(source=orig_image, show=False)[0] # Prediction and return a list of dict with all information

            data = []
            # print(results)
            if len(results.keypoints) > 0:
                print(results.names)
                for idx, keyspoints in enumerate(results.keypoints):
                    data.append({
                        'x_rs': keyspoints[5][0],
                        'y_rs': keyspoints[5][1],
                        'x_ls': keyspoints[6][0],
                        'y_ls': keyspoints[6][1],
                        'x_rh': keyspoints[9][0], 
                        'y_rh': keyspoints[9][1],
                        'x_lh': keyspoints[10][0],
                        'y_lh': keyspoints[10][1],
                        'bbox_c1': [int(a) for a in results.boxes.xyxy[idx]]
                        })

            # state.findHandSign(results)
            # state.findCurrentBBox(results)

            # if state.isTracking():
            #     val1, val2 = state.calc()
            #     fileW.writeFile([val1, val2])
            
            colors = [
                (0, 0, 255),
                (0, 255, 255),
                (255, 255, 0),
                (255, 0, 255),
                (255, 0, 0)
            ]
            if (show_output):
                radius = 5
                for (i, elt) in enumerate(data):
                    cv2.circle(orig_image, (int(elt["x_rs"]), int(elt["y_rs"])), radius, colors[i%5], -1)
                    cv2.circle(orig_image, (int(elt["x_ls"]), int(elt["y_ls"])), radius, colors[i%5], -1)
                    cv2.circle(orig_image, (int(elt["x_rh"]), int(elt["y_rh"])), radius, colors[i%5], -1)
                    cv2.circle(orig_image, (int(elt["x_lh"]), int(elt["y_lh"])), radius, colors[i%5], -1)
                    cv2.rectangle(orig_image, elt["bbox_c1"][0:2], elt["bbox_c1"][2:4], colors[i%5], 2)

                # if state.currentBoundingBox != None:
                    # print("printed BBBBBBOX : ", state.currentBoundingBox)
                    # cv2.rectangle(orig_image, state.currentBoundingBox[0:2], state.currentBoundingBox[2:4], (0, 255, 0), 2)
                
                cv2.imshow("Render", orig_image)
                k = cv2.waitKey(33)
                if k==27: return # Esc key to stop

                # print(state.currentBoundingBox)

            # state.prepareToNextFrame()
            
            
            

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--poseweights', nargs='+', type=str, default='weights/yolov8s-pose.pt', help='model path(s)')
    parser.add_argument('--device', type=str, default='cpu', help='cpu/0,1,2,3(gpu)')   #device arugments
    parser.add_argument('--show_output', action=argparse.BooleanOptionalAction)
    opt = parser.parse_args()
    return opt


#main function
def main(opt):
    run(**vars(opt))

if __name__ == "__main__":
    opt = parse_opt()
    # strip_optimizer(opt.device,opt.poseweights)
    main(opt)
