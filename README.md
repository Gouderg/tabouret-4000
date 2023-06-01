# Tabouret 3000

## Faire un enviro

## Comment faire marcher la caméra

Installer le paquet depthai

## Bibliography

## Camera
https://medium.com/augmented-startups/opencv-ai-kit-an-introduction-to-oak-1-and-oak-d-4debb66175ca

- [ ] Récupérer des images de la caméra


## Yolov8

- [ ] Entrainé


## Algorithme pour la raspberry.

https://docs.luxonis.com/projects/hardware/en/latest/pages/guides/raspberrypi.html





## ROADMAP

- [ ] Allumer la caméra et donner l'image au 2 algo
- [ ] Fine-tuned pour détecter uniquement la personne. => https://www.kaggle.com/datasets/constantinwerner/human-detection-dataset
- [ ] Essayer de garder la valeur de la personne en mémoire
- [ ] Entraîner un modèle pour reconnaître les gestes de la main => https://www.kaggle.com/datasets/gti-upm/leapgestrecog
- [ ] Faire un algo qui calcule de la distance de l'image


## Lien Utile:

* [Exemple de training luxonis x yolov8](https://github.com/luxonis/depthai-ml-training/blob/master/colab-notebooks/YoloV8_training.ipynb)
* [Convertir le .pt en blob](http://tools.luxonis.com/)
* []



## All command

train for the sign_recognition: 

```bash
yolo train imgsz=640 batch=-1 epochs=50 data=mix_hand.yaml model=yolov8s.pt device=0 cache=ram
yolo train imgsz=640 batch=-1 epochs=50 data=hand_data.yaml model=yolov8s.pt device=0 cache=ram
yolo train imgsz=640 batch=16 epochs=50 data=budokai.yaml model=hand_robo.pt device=0 cache=ram
yolo train imgsz=640 batch=16 epochs=50 data=hand.yaml model=yolov8s.pt device=0 cache=ram



```
just detect on normal yolo:

```bash
yolo predict source=0 show=True classes=0
yolo predict source=0 show=True model="../models/mixIsenRobo/mixIsenRobo.onnx"

```

tracking personn:

```bash
yolo track source=0 show=True classes=0 tracker="bytetrack.yaml"

```

Pose estimation avec yolov7 : https://github.com/WongKinYiu/yolov7/

python detect.py --weights ../models/pose/yolov7-w6-pose.pt --source 0 --img-size 640 --view-img




=> Faire une réduction en réduisant la taille de la main sur l'image






###



