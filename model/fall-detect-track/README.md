<h1> Human Falling Detection and Tracking </h1>

Using Tiny-YOLO oneclass to detect each person in the frame and use 
[AlphaPose](https://github.com/MVIG-SJTU/AlphaPose) to get skeleton-pose and then use
[ST-GCN](https://github.com/yysijie/st-gcn) model to predict action from every 30 frames 
of each person tracks.

Which now support 7 actions: Standing, Walking, Sitting, Lying Down, Stand up, Sit down, Fall Down.

<div align="center">
    <img src="sample1.gif" width="416">
</div>
<div align="center">
    <video src="output/output.mp4"></video>
</div>

## Prerequisites

- Python > 3.6
- Pytorch > 1.3.1

Original test run on: i9-10900K CPU @ 3.70GHz, GeForce RTX 2080 8GB, CUDA 10.2

## Data

This project has trained a new Tiny-YOLO oneclass model to detect only person objects and to reducing 
model size. Train with rotation augmented [COCO](http://cocodataset.org/#home) person keypoints dataset 
for more robust person detection in a variant of angle pose.

For actions recognition used data from [Le2i](http://le2i.cnrs.fr/Fall-detection-Dataset?lang=fr)
Fall detection Dataset (Coffee room, Home) extract skeleton-pose by AlphaPose and labeled each action 
frames by hand for training ST-GCN model.

## Pre-Trained Models

- Tiny-YOLO oneclass - [.pth](https://drive.google.com/file/d/1obEbWBSm9bXeg10FriJ7R2cGLRsg-AfP/view?usp=sharing),
  [.cfg](https://drive.google.com/file/d/19sPzBZjAjuJQ3emRteHybm2SG25w9Wn5/view?usp=sharing)  
  备用：[.pth](https://www.aliyundrive.com/s/sKWeJvHmBcY)，下载后文件名删除`.txt`
- SPPE FastPose (AlphaPose) - [resnet101](https://drive.google.com/file/d/1N2MgE1Esq6CKYA6FyZVKpPwHRyOCrzA0/view?usp=sharing),
  [resnet50](https://drive.google.com/file/d/1IPfCDRwCmQDnQy94nT1V-_NVtTEi4VmU/view?usp=sharing)  
  备用：[resnet101](https://www.aliyundrive.com/s/PUJRs6oqNF3)，[resnet50](https://www.aliyundrive.com/s/4aLJRUuGL3b)，下载后文件名删除`.txt`
- ST-GCN action recognition - [tsstg](https://drive.google.com/file/d/1mQQ4JHe58ylKbBqTjuKzpwN2nwKOWJ9u/view?usp=sharing)  
  备用：[tsstg](https://www.aliyundrive.com/s/uqUACkT4eug)，下载后文件名删除`.txt`

## Basic Use

1. Download all pre-trained models into ./Models folder.
2. Run main.py
```
    python main.py ${video file or camera source}
```

## Reference

- AlphaPose : https://github.com/Amanbhandula/AlphaPose
- ST-GCN : https://github.com/yysijie/st-gcn

## Origin

[GajuuzZ/Human-Falling-Detect-Tracks](https://github.com/GajuuzZ/Human-Falling-Detect-Tracks)

