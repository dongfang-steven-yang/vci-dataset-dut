# Vehicle-Crowd Intraction (VCI) - DUT Dataset
Top-view trajectory data of pedestrians in crowd under vehicle influence in everyday campus scenarios

* Last updated on 03/07/2019
* E-mail: yang.3455@osu.edu

![](osu-logo.jpg)
* Control and Intelligent Transportation Research (CITR) Lab
* Department of Electrical and Computer Engineering
* Center for Automotive Research (CAR)

## Note

A sister dataset of pedestrian trajectories, CITR dataset, which comes from controlled experiments of fundamental vehicle-crowd interaction, can be accessed at [here](https://github.com/dongfang-steven-yang/vci-dataset-citr).

The detailed description of both datasets can be accessed at arXiv preprint: [Top-view Trajectories: A Pedestrian Dataset of Vehicle-Crowd Interaction from Controlled Experiments and Crowded Campus](https://arxiv.org/abs/1902.00487).

This paper was submitted to [The 30th IEEE Intelligent Vehicles Symposium in Paris](http://iv2019.org/). 

If you find the dataset useful, please consider citing the above paper. :grinning:

## Overview

The DUT dataset was collected at two crowded locations in the campus of Dalian University of Technology (DUT) in China. When a crowd of pedestrians interact with a vehicle, there is no priority (the right of way) for either pedestrians or the vehicle.

* One location includes an area of pedestrian crosswalk at an intersection without traffic signals.  
* The other location is a relatively large shared space, in which pedestrians and vehicles can freely move. 

A DJI Mavic Pro Drone with a down-facing camera was hovering above the interested area as the recording equipment, high enough to be unnoticed by pedestrians and vehicles. The video resolution is 4K with an fps of 23.98. Pedestrians are primarily made up of college students who just finished classes and on their way out of classrooms. Vehicles are regular cars that go through the campus. 

A video clip with both the pedestrains and vehicles labeled is shown below:
[![DUT Dataset Demo](http://img.youtube.com/vi/ia9kVPBLXJI/0.jpg)](https://www.youtube.com/watch?v=ia9kVPBLXJI "DUT Dataset Demo")

## Download Stabilized Raw Videos
The stabilized raw videos of DUT dataset can be downloaded at [this Google Drive link](https://drive.google.com/file/d/19kPIvMshynDSrHbnPEt3qvvqCdPrhmZ6/view?usp=sharing).

## Scenarios

- 17 clips of crosswalk sceanrio
- 11 clips of shared space scenario
- 1793 pedestrian trajectories in total

## Dataset Desription

"clips" folder contains the following subfolders:

- backgrounds: store the generated background of each video clip (the size is in accordance with the ROI size) after running "vis_and_demo.py"
- ratios: files for the ratio that converts pixels into meters
- roi_clips: store the generated video of each video clip after running "vis_and_demo.py"
- rois: files for the region of interest (ROI)
- stabilized: stabilized video clips
- trajectories_filtered: pedestrian trajectory data files

Inside the "trajectories_filtered" folder, each clip has two .csv files, one for pedestrian trajectories and one for vehicle trajectories. For each .csv file, the first row is the header. 

For pedestrians, each column of the header means:

```
id: 
x: tracked x position in pixels (unfiltered)
y: tracked y position in pixels (unfiltered)
frame: frame number from the video clip
label: "ped" means pedestrian
x_est: x position estimated by Kalman filter
y_est: y position estimated by Kalman filter
vx_est: x velocity estimated by Kalman filter 
vy_est: y velocity estimated by Kalman filter
```

For vehicles, each column of the header means:
```
id: 
x_c: x position of the vehicle center point (calculated) in pixels (unfiltered)
y_c: y position of the vehicle center point (calculated) i in pixels (unfiltered)
x_fl, x_fr, x_rr, x_rl, y_fl, y_fr, y_rr, y_rl: tracking points (in general you don't have to care about these points, just use the center point or the filtered trajectories)
frame: frame number from the video clip
label: "veh" means vehicle
x_est: x position estimated by Kalman filter
y_est: y position estimated by Kalman filter
vx_est: x velocity estimated by Kalman filter 
vy_est: y velocity estimated by Kalman filter
```

## Python scripts for visualizing data and generating demo videos

There is a python script for visualizing the dataset. You need to intall following prerequisites to run the python script: 

```
pandas
matplotlib
opencv (tested version: 3.4.2)
```

After installing the prerequisite, run the following command:

```
vis_and_demo.py --source ../clips/stabilized/ --filtered_traj ../clips/trajectories_filtered/ --roi ../clips/rois/ --roi_clip ../clips/roi_clips/ --background ../clips/backgrounds/
```

## Linked Paper

The correspoding paper of the dataset was submitted to the 30th IEEE Intelligent Vehicles Symposium. 

arXiv preprint: [Top-view Trajectories: A Pedestrian Dataset of Vehicle-Crowd Interaction from Controlled Experiments and Crowded Campus](https://arxiv.org/abs/1902.00487)


## Errors
- If you find any errors, please contact the author.
