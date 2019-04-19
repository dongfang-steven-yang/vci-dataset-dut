## Dataset Desription Legacy

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