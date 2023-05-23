import cv2
import numpy as np
from torchvision import transforms
from utils.datasets import letterbox
from utils.torch_utils import select_device
from models.experimental import attempt_load
from utils.general import non_max_suppression_kpt
import torch


class CustomModel:

    def __init__(self, device, poseweights):
        self.device = select_device()
        self.model = attempt_load(poseweights, map_location=self.device)
        _ = self.model.eval()
        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names  # get class names

    def loadModel(self):
        pass

    def predict(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) #convert frame to RGB
        image = letterbox(image, (640), stride=64, auto=True)[0]

        # Reshape (640, 640, 3) to (1, 3, 640, 640)
        image = transforms.ToTensor()(image)    
        image = torch.tensor(np.array([image.numpy()]))

        image = image.to(self.device)  #convert image data to device
        image = image.float() #convert image to float precision (cpu)


        with torch.no_grad():  #get predictions
            output_data, _ = self.model(image)

        output_data = non_max_suppression_kpt(output_data,   #Apply non max suppression
                                    0.25,   # Conf. Threshold.
                                    0.65, # IoU Threshold.
                                    nc=self.model.yaml['nc'], # Number of classes.
                                    nkpt=self.model.yaml['nkpt'], # Number of keypoints.
                                    kpt_label=True)
        


        results = []
        steps = 3
        for _, pose in enumerate(output_data):  # detections per image
            bboxes = pose[:, :6]  # bounding boxes

            if len(output_data):  #check if no pose
                # for c in pose[:, 5].unique(): # Print results
                #     n = (pose[:, 5] == c).sum()  # detections per class
                #     print("No of Objects in Current Frame : {}".format(n))
                
                for det_index, (*xyxy, conf, cls) in enumerate(reversed(pose[:,:6])): #loop over poses for drawing on frame
                    c = int(cls)  # integer class
                    kpts = pose[det_index, 6:]
                    
                    label = f'{self.names[c]} {conf:.2f}'


                    '''
                        5: right_shoulder
                        6: left_shoulder
                        9: right_hand
                        10: left_hand

                    '''
                    
                    results.append({
                        'x_rs': kpts[steps * 5],
                        'y_rs': kpts[steps * 5 + 1],
                        'x_ls': kpts[steps * 6],
                        'y_ls': kpts[steps * 6 + 1],
                        'x_rh': kpts[steps * 9], 
                        'y_rh': kpts[steps * 9 + 1],
                        'x_lh': kpts[steps * 10],
                        'y_lh': kpts[steps * 10 + 1],
                        'bbox_c1': [int(a) for a in bboxes[det_index]],
                        'label': label
                    })

            return results
        

