# Car Guardian

## Project Background
The primary issue we are addressing stems from the increased average age of cars on the road, standing at 12.5 years. This implies that a significant portion of cars lacks modern safety features. Since 63% of vehicles in the United States predate 2015, a majority of drivers face heightened vulnerability, lacking crucial safety advancements to mitigate risks effectively. The main objective of our project was to equip older cars with new safety features that they lack in order to increase the safety of drivers on the road, and decrease the amount of information that a driver needs to keep track of while driving. 

## Project Requirements
Main Features: Pre-collision detection, Traffic light detection, Intelligent video clipping and standard dash cam features

Object Detection: 85% accuracy in detection, The calculated distances using YOLO is within a 10% margin of error from the actual distance

Traffic Obstacle Detection: Detect the color of traffic lights and stop signs with a 95% accuracy, Light detection at distances high enough for appropriate braking distance depending on distance

## Project Results
### Pre-collision Detection Demo Video
https://drive.google.com/file/d/10GGkSJfenU6cbIF_fhn91VDZYzM1X13A/view?usp=sharing

### Traffic Obstacle Detection Demo
https://drive.google.com/file/d/1cJTCRGgr-AKXftDhSrfZo4vX_noMZuZC/view?usp=sharing

### GUI Functionality Video Demo
https://drive.google.com/file/d/1h3RFA_9uvHDd9rbV4NpVV3qNjaVmApRX/view?usp=sharing


### Hardware Installation
1. Plug in a 1080p logitech camera into the laptop
2. Plug the 7in LCD screen into the laptop
3. Plug the car’s power adapter into the laptop
4. Plug the OBD port into laptop

### Software Installation Steps
Install VSCode
Install Python3 from https://www.python.org/downloads/

Install ultralytics by cloning the yolo v8 github at https://github.com/ultralytics/ultralytics

To install OpenCV use this command for Windows.
```
pip install opencv-contrib-python
```
To install ultralytics use this command.
```
pip install ultralytics
```
This install is used to send POST requests for the audible alerts.
```
pip install requests
```
This is a Tensor library like NumPy, with strong GPU support.
```
pip install torch
```
This is used for the GUI as it is a web application framework.
```
pip install flask
```
This is required if you want to utilize CUDA to improved performance. Utilizing only the CPU is possible, but, for the best performance, it is recommended to install the newest version of CUDA and Pytorch.
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

