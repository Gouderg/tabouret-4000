import ultralytics as ul

class CustomModel:

    def __init__(self, device, poseweights):
        ul.checks()
        self.device = device
        self.model = ul.YOLO(poseweights)

    def predict(self, frame):

        results = self.model.predict(show=False, source=frame, device=self.device)[0]
        data = []
        if len(results.keypoints) > 0:
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
        return data