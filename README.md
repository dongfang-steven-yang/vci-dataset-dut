# Vehicle-Crowd Intraction (VCI) - DUT Dataset
Top-view trajectory data of pedestrians in crowd under vehicle influence in everyday campus scenarios

* Last updated on 04/19/2019
* E-mail: yang.3455@osu.edu

<img src="osu-logo.jpg" width="500">

* Control and Intelligent Transportation Research (CITR) Lab
* Department of Electrical and Computer Engineering
* Center for Automotive Research (CAR)

## Note

**A major update was done on Apr 19, 2019. An extended Kalman filter was applied for refining the vehicle trajectory, so that the output vehicle state contains (x, y, heading, speed), which is in accordance with a vehicle model (bicycle model).**

A sister dataset of pedestrian trajectories, CITR dataset, which comes from controlled experiments of fundamental vehicle-crowd interaction, can be accessed at [here](https://github.com/dongfang-steven-yang/vci-dataset-citr).

The detailed description of both datasets can be accessed at arXiv preprint: [Top-view Trajectories: A Pedestrian Dataset of Vehicle-Crowd Interaction from Controlled Experiments and Crowded Campus](https://arxiv.org/abs/1902.00487).

This paper was accepted to [The 30th IEEE Intelligent Vehicles Symposium in Paris](http://iv2019.org/). 

If you find the dataset useful, please consider citing the above paper. :grinning:

## Overview

The DUT dataset was collected at two crowded locations in the campus of Dalian University of Technology (DUT) in China. When a crowd of pedestrians interact with a vehicle, there is no priority (the right of way) for either pedestrians or the vehicle.

* One location includes an area of pedestrian crosswalk at an intersection without traffic signals.  
* The other location is a relatively large shared space, in which pedestrians and vehicles can freely move. 

A DJI Mavic Pro Drone with a down-facing camera was hovering above the interested area as the recording equipment, high enough to be unnoticed by pedestrians and vehicles. The video resolution is 4K with an fps of 23.98. Pedestrians are primarily made up of college students who just finished classes and on their way out of classrooms. Vehicles are regular cars that go through the campus. 

A video clip with both the pedestrains and vehicles labeled is shown below:

[![DUT Dataset Demo](http://img.youtube.com/vi/ia9kVPBLXJI/0.jpg)](https://www.youtube.com/watch?v=ia9kVPBLXJI "DUT Dataset Demo")

Or you can download it [here](https://github.com/dongfang-steven-yang/vci-dataset-dut/raw/master/demo-dut.mp4)

<video width="700" height="400" controls>
  <source src="/demo-dut.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>


## Download Stabilized Raw Videos
The stabilized raw videos of DUT dataset can be downloaded at following links:
[Google Drive Download](https://drive.google.com/open?id=1J0PW4NoL2mi_eaN_8_SgkWkc0rk7MJZC).
[Baidu Yun Download](https://pan.baidu.com/s/1lP-qE3lAJuLDwN3H6ee26Q). Code: ui9a


## Scenarios

- 17 clips of crosswalk sceanrio
- 11 clips of shared space scenario
- 1793 pedestrian trajectories in total

## Description of The DUT Repository

### Dataset in `\data`

`\backgrounds`: background of each clip, with a cropped size, which is in accordance with the data (for visualization you still need to convert from meters to pixels by ratio/scale file).

`\figures`: an overview of all trajectories for each video clip

`\ratios`: files for the ratio\scale that converts between pixel coordinates (1920x1080) and coordinates in meters. All the recorded trajectories have already been converted in meters. 

Raw `\trajectroies` and `\trajectroies_filtered`: inside both folders, each video clip has two `.csv` files, one for pedestrian trajectories and one for vehicle trajectories. For each `.csv` file, the first row is the header. 

#### Filtered Trajectories

We recommend you to use data in `\trajectories_filtered`. Below is the header description:

For pedestrian `.csv`: 
```
id: pedestrian id
frame: frame number of the video clip
label: 'ped' means pedestrian
x_est: estiamted x position
y_est: estimated y position
xv_est: estiamted velocity in x axis
yv_est: estimated velocity in y axis
```

For vehicle `.csv`: 
```
id: vehicle id
frame: frame number of the video clip
label: 'veh' means vehicle
x_est: estiamted x position
y_est: estimated y position
psi_est: orientation (heading angle) of the vehicle (in rad)
vel_est: longitudinal velocity of the vehicle
```

#### Filtered Trajectories

If you would like to use raw `\trajectroies`:

For pedestrians:
```
id: pedestrian id
x: tracked x position (unfiltered)
y: tracked y position (unfiltered)
frame: frame number of the video clip
label: "ped" means pedestrian
```

For vehicles:
```
id: vehicle id
x_c: x position of the vehicle center point (calculated)
y_c: y position of the vehicle center point (calculated)
x_fl, x_fr, x_rr, x_rl, y_fl, y_fr, y_rr, y_rl: tracking points (in general you don't have to care about these points, just use the center point or the filtered trajectories)
frame: frame number of the video clip
label: "veh" means vehicle
```

## Filters and Tools

The data has already been filtered, so you don't have to do it again. We just provide them for your refernce. 

These are python codes for filtering the raw data `filter_trajectories.py` and generating statistics `statistics.py`. The Kalman filters were implemented in `tools\kalman_filters.py`.


## Errors
- If you find any errors, please contact the author.
