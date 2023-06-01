import argparse
import depthai as dai
from camera import Camera
from model import CustomModel
from state import State
from fileWriter import FileWriter
import time
import cv2
from datetime import datetime


colors = [
    (0, 0, 255),
    (0, 255, 255),
    (255, 255, 0),
    (255, 0, 255),
    (255, 0, 0)
]

def run(poseweights, device, save_output):

    camera = Camera()
    model = CustomModel(device, poseweights)
    fileW = FileWriter("coucou")
    state = State()

    fileW.clean()

    # Connect to device and start pipeline
    with dai.Device(camera.pipeline) as deviceCamera:
         
        # Print camera information
        camera.printInformation(deviceCamera)

        # Output queue will be used to get the rgb frames from the output defined above
        qRgb = deviceCamera.getOutputQueue(name="rgb", maxSize=4, blocking=False)

        cpt = 0
        
        while True:
            start = time.time()
            inRgb = qRgb.get()  # blocking call, will wait until a new data has arrived

            orig_image = inRgb.getCvFrame() 

            results = model.predict(orig_image) # Prediction and return a list of dict with all information

            state.findHandSign(results)
            state.findCurrentBBox(results)

            if state.isTracking():
                val1, val2 = state.calc()
                fileW.writeFile([val1, val2])

                if save_output:
                    radius = 5
                    for (i, elt) in enumerate(results):
                        cv2.circle(orig_image, (int(elt["x_rs"]), int(elt["y_rs"])), radius, colors[i%5], -1)
                        cv2.circle(orig_image, (int(elt["x_ls"]), int(elt["y_ls"])), radius, colors[i%5], -1)
                        cv2.circle(orig_image, (int(elt["x_rh"]), int(elt["y_rh"])), radius, colors[i%5], -1)
                        cv2.circle(orig_image, (int(elt["x_lh"]), int(elt["y_lh"])), radius, colors[i%5], -1)
                        cv2.rectangle(orig_image, elt["bbox_c1"][0:2], elt["bbox_c1"][2:4], colors[i%5], 2)
                    
                    heure_str = datetime.now().strftime("%Y%m%d_%H:%M:%S")
                    cv2.imwrite("img/{}_{}.png".format(heure_str, cpt), orig_image)
                    cpt += 1

            else:
                fileW.writeFile([0, 0])

            state.prepareToNextFrame()
            end = time.time()
            print("Next frame, time elapsed: ", end-start)
            
            
            

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--poseweights', nargs='+', type=str, default="yolov8n-pose.pt", help='model path(s)')
    parser.add_argument('--device', type=str, default='0', help='cpu/0,1,2,3(gpu)')   #device arugments
    parser.add_argument('--save-output', action='store_true')
    # parser.add_argument('--show_output', action=argparse.BooleanOptionalAction)
    opt = parser.parse_args()
    return opt


#main function
def main(opt):
    run(**vars(opt))

if __name__ == "__main__":
    opt = parse_opt()
    main(opt)