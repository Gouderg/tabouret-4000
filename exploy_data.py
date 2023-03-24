import cv2
import time
import torch
import argparse
import numpy as np
import matplotlib.pyplot as plt
from torchvision import transforms
from utils.datasets import letterbox
from utils.torch_utils import select_device
from models.experimental import attempt_load
from utils.general import non_max_suppression_kpt,strip_optimizer,xyxy2xywh
from utils.plots import output_to_keypoint, plot_skeleton_kpts,colors,plot_one_box_kpt
import depthai as dai

@torch.no_grad()
def run(poseweights="yolov7-w6-pose.pt",device='cpu',view_img=False,
        save_conf=False,line_thickness = 3,hide_labels=False, hide_conf=True):


    
    device = select_device(opt.device) #select device
    half = device.type != 'cpu'

    model = attempt_load(poseweights, map_location=device)  #Load model
    _ = model.eval()
    names = model.module.names if hasattr(model, 'module') else model.names  # get class names

    frame = cv2.imread("data/handUp.png")
       
    orig_image = frame #store frame
    image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB) #convert frame to RGB
    image = letterbox(image, (640), stride=64, auto=True)[0]

    # Reshape (640, 640, 3) to (1, 3, 640, 640)
    image = transforms.ToTensor()(image)    
    image = torch.tensor(np.array([image.numpy()]))

    image = image.to(device)  #convert image data to device
    image = image.float() #convert image to float precision (cpu)


    with torch.no_grad():  #get predictions
        output_data, _ = model(image)

    output_data = non_max_suppression_kpt(output_data,   #Apply non max suppression
                                0.25,   # Conf. Threshold.
                                0.65, # IoU Threshold.
                                nc=model.yaml['nc'], # Number of classes.
                                nkpt=model.yaml['nkpt'], # Number of keypoints.
                                kpt_label=True)

    

    im0 = image[0].permute(1, 2, 0) * 255 # Change format [b, c, h, w] to [h, w, c] for displaying the image.
    im0 = im0.cpu().numpy().astype(np.uint8)
    
    im0 = cv2.cvtColor(im0, cv2.COLOR_RGB2BGR) #reshape image format to (BGR)

    for i, pose in enumerate(output_data):  # detections per image

        if len(output_data):  #check if no pose
            for c in pose[:, 5].unique(): # Print results
                n = (pose[:, 5] == c).sum()  # detections per class
                print("No of Objects in Current Frame : {}".format(n))
            
            for det_index, (*xyxy, conf, cls) in enumerate(reversed(pose[:,:6])): #loop over poses for drawing on frame
                c = int(cls)  # integer class
                kpts = pose[det_index, 6:]
                label = None if opt.hide_labels else (names[c] if opt.hide_conf else f'{names[c]} {conf:.2f}')


                '''
                    5: right_shoulder
                    6: left_shoulder
                    9: right_hand
                    10: left_hand

                '''
                steps = 3
                radius = 5
                x_rs, y_rs = kpts[steps * 5], kpts[steps * 5 + 1]
                x_ls, y_ls = kpts[steps * 6], kpts[steps * 6 + 1]
                x_rh, y_rh = kpts[steps * 9], kpts[steps * 9 + 1]
                x_lh, y_lh = kpts[steps * 10], kpts[steps * 10 + 1]

                    
                if (y_lh < y_ls): print("Main gauche levé")
                if (y_rh < y_rs): print("Main droite levé")

                print(label)

                cv2.circle(im0, (int(x_rs), int(y_rs)), radius, (0, 0, 255), -1)
                cv2.circle(im0, (int(x_ls), int(y_ls)), radius, (0, 0, 255), -1)
                cv2.circle(im0, (int(x_rh), int(y_rh)), radius, (0, 0, 255), -1)
                cv2.circle(im0, (int(x_lh), int(y_lh)), radius, (0, 0, 255), -1)
                
                
                c1, c2 = (int(xyxy[0]), int(xyxy[1])), (int(xyxy[2]), int(xyxy[3]))
                tl = line_thickness or round(0.002 * (im0.shape[0] + im0.shape[1]) / 2) + 1  # line/font thickness
                cv2.rectangle(im0, c1, c2, (255,0,0), thickness=tl*1//3, lineType=cv2.LINE_AA)

    # cv2.imshow("YOLOv7 Pose Estimation Demo", im0)
    
    # while cv2.waitKey(1) != ord("q"):
    #     continue



def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--poseweights', nargs='+', type=str, default='weights/yolov7-w6-pose.pt', help='model path(s)')
    parser.add_argument('--device', type=str, default='cpu', help='cpu/0,1,2,3(gpu)')   #device arugments
    parser.add_argument('--view-img', action='store_true', help='display results')  #display results
    parser.add_argument('--save-conf', action='store_true', help='save confidences in --save-txt labels') #save confidence in txt writing
    parser.add_argument('--line-thickness', default=3, type=int, help='bounding box thickness (pixels)') #box linethickness
    parser.add_argument('--hide-labels', default=False, action='store_true', help='hide labels') #box hidelabel
    parser.add_argument('--hide-conf', default=False, action='store_true', help='hide confidences') #boxhideconf
    opt = parser.parse_args()
    return opt


#main function
def main(opt):
    run(**vars(opt))

if __name__ == "__main__":
    opt = parse_opt()
    strip_optimizer(opt.device,opt.poseweights)
    main(opt)

