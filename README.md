# Car Guardian

## Project Background
The primary issue we are addressing stems from the increased average age of cars on the road, standing at 12.5 years. This implies that a significant portion of cars lacks modern safety features. Since 63% of vehicles in the United States predate 2015, a majority of drivers face heightened vulnerability, lacking crucial safety advancements to mitigate risks effectively. The main objective of our project was to equip older cars with new safety features that they lack in order to increase the safety of drivers on the road, and decrease the amount of information that a driver needs to keep track of while driving. 

## Project Requirements
Main Features: Pre-collision detection, traffic light detection, stop sign detection, intelligent video clipping and standard dash cam features

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

### Installing Cuda
To use CUDA on your system, you will need the following installed:
- A CUDA-capable GPU
- This would be all NVIDIA GeForce, Quadro, and Tesla GPUs
- NVIDIA CUDA Toolkit (available at https://developer.nvidia.com/cuda-downloads)
- A supported version of Linux with a gcc compiler and toolchain (if on Linux)

To check if your GPU is compatible with CUDA:
- On Windows, you can verify that you have a CUDA-capable GPU through the Display Adapters section in the Windows Device Manager. Here you will find the vendor name and model of your graphics card(s). If you have an NVIDIA card that is listed in https://developer.nvidia.com/cuda-gpus, that GPU is CUDA-capable. The Release Notes for the CUDA Toolkit also contain a list of supported products.
- The Windows Device Manager can be opened via the following steps:
  1. Open a run window from the Start Menu
  2. control /name Microsoft.DeviceManager
- To check on either operating system, you can visit https://developer.nvidia.com/cuda-gpus to see if your GPU is on the approved list provided by NVIDIA. 

### Verifying CUDA Installation
- Open a command prompt (on Windows) or a terminal (on Linux).
- Type nvcc --version and press Enter.
- If CUDA is installed correctly, you should see the version of the CUDA Toolkit that is installed, along with the version of the NVIDIA GPU driver.

### Installing Pytorch
- To install Pytorch on Windows or Linux using pip, use the command provided:
``` 
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118.
```
- For any other configurations, visit https://pytorch.org/get-started/locally/ for more information on Pytorch installation. The Pytorch documentation provides installation instructions for different versions of CUDA and for those who prefer technologies like conda rather than pip.

### Verifying Pytorch Installation
To ensure that PyTorch was installed correctly, we can verify the installation by running sample PyTorch code. Here we will construct a randomly initialized tensor.
From the command line, type: 
```
python
```
Then:
```
import torch
x = torch.rand(5, 3)
print(x)
```
The output should be something similar to:
```
tensor([[0.3380, 0.3845, 0.3217],
        [0.8337, 0.9050, 0.2650],
        [0.2979, 0.7141, 0.9069],
        [0.1449, 0.1132, 0.1375],
        [0.4675, 0.3947, 0.1426]])
```
### Testing Pytorch with CUDA in Python
The following code can be run if Pytorch is able to detect your GPU:
```
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Using device:', device)
print()
```
This code would produce an output like this:
```
Using device: cuda
```
To get additional info when using CUDA:
```
#Additional Info when using cuda
if device.type == 'cuda':
    print(torch.cuda.get_device_name(0))
    print('Memory Usage:')
    print('Allocated:', round(torch.cuda.memory_allocated(0)/1024**3,1), 'GB')
    print('Cached:   ', round(torch.cuda.memory_reserved(0)/1024**3,1), 'GB')
```
This code would output like this:
```
Tesla K80
Memory Usage:
Allocated: 0.3 GB
Cached:    0.6 GB
```
### To Use Your Device’s CPU instead of GPU
In our code, we have two locations you would want to alter the code in order to use the CPU rather than the GPU. 
The first would be in FocalCalculation.py:

![image](https://github.com/sraja1114/YOLOv4-distance-tracking/assets/123511793/26f21ee7-ccfc-41c0-be41-3a345bc20b9d)

On line 28, you would want to change the code so it reads as follows:
```
device = 'cpu'
print(f'Using device: {device}')
model = YOLO('yolov8n.pt').to(device)
```

The second change is in mainOBD.py:

![image](https://github.com/sraja1114/YOLOv4-distance-tracking/assets/123511793/fc79e50a-a0d1-423d-9c8b-929695b287da)

On line 204, you want the code to be similar to before:
```
device = 'cpu'
print(f'Using device: {device}')
model = YOLO('yolov8n.pt').to(device)
```

### OBS Studio Instructions
The next piece of software that should be installed is OBS Studio. OBS Studio’s virtual camera feature was used to allow multiple programs to use the webcam simultaneously. Below will be the installation instruction and setup process.

To install OBS Studio, visit the following website to download executable for your operating system: https://obsproject.com/download.

### Creating the Scene
1. Navigate to File > Settings to set up the video output to the correct resolution.
2. Go to the “Video” tab and edit the resolution to be 1440x1080. This allows us to use the full 4:3 image that the sensor of the camera is receiving.
3. Next, exit out of the settings and click the “Add Scene” button in the “Scenes” window in the bottom left of the screen. Then, enter a name for the scene.
4. After that, click “Add Sources” in the “Sources” window on the right of the “Scene” Window. 
5. Then, add the webcam as a “Video Capture Device”. Afterward, set a name for the source, and then select “Logitech 1080p Stream” as the device in the window that appears with the remaining inputs left as default.
6. The webcam should now appear in the “Sources” window as shown below. The visibility of the camera can be toggle on and off with the eye button. (You can also add any prerecorded videos and images if you wish to test the output of the code. This feature was used throughout the testing of our final product.)
7. Lastly, in the “Controls” window in the bottom right. Click the “Start Virtual Camera” button to output the video as a webcam.

### Choosing the OBS Virtual Camera as the Video Source 
In mainOBD.py, go to line 224 to update the source that YOLO uses for it’s calculations.

![image](https://github.com/sraja1114/YOLOv4-distance-tracking/assets/123511793/0625cb50-4cf1-4e3e-b9bd-7d5a7a343e2b)

The number provided to the VideoCapture(index) is the sourced used in the program. If you have a webcam built into your device, such as for a Laptop, it will likely be at index 2 (0 being the default camera, 1 being the feed from the attached webcam, and 2 being the virtual camera from OBS). If there are no default cameras, the OBS Virtual Webcam will likely be at index 1. Below is a function that can be used to see the valid video camera on your device.
```
def returnCameraIndexes():
    # checks the first 10 indexes.
    index = 0
    arr = []
    i = 10
    while i > 0:
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            arr.append(index)
            cap.release()
        index += 1
        i -= 1
    return arr
```
### React.js OBS Virtual Webcam Setup
For the React.js frontend, in order to change the camera, you alter the browser settings. Make sure to allow localhost to access the camera and microphone. Below is where to change the settings if you are using Chrome as your browser. Navitage to Settings > Privacy and settings > Site settings > Camera. If you are using another browser, the camera options should also be available in your browser settings.

### OBDWiz Setup Instructions


### Operation Instructions

