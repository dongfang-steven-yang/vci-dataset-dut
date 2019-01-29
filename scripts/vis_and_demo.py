# -*- coding: utf-8 -*-
"""
Updated on: Jan 18, 2019
@author: Dongfang Yang
@email: yang.3455@osu.edu

This script is used for visualizing trajectories and generate demo videos.
"""

import cv2
import sys
import os
import pickle
import argparse
import pandas
from modules_dvp import generate_background
import matplotlib.pyplot as plt

pandas.set_option('display.max_columns', 10)

if __name__ == '__main__':
    # argument parsing
    ap = argparse.ArgumentParser()
    ap.add_argument('-s', '--source', required=True, help='relative path of source videos directory')
    ap.add_argument('-f', '--filtered_traj', required=True, help='relative path of output trajectories directory')
    ap.add_argument('-r', '--roi', required=True, help='relative path of storing ROIs')
    ap.add_argument('-c', '--roi_clip', required=True, help='relative path of output clipped videos')
    ap.add_argument('-b', '--background', required=True, help='relative path of backgrounds')
    args = vars(ap.parse_args())

    # interpreting arguments: Directories
    dir_relative_source = args['source']
    dir_relative_filtered_trajs = args['filtered_traj']
    dir_relative_rois = args['roi']
    dir_relative_clipped = args['roi_clip']
    dir_relative_backgrounds = args['background']

    print('Working directory is:'+os.getcwd())
    print('Input video relative directory is:' + dir_relative_source)
    print('Background relative directory is:' + dir_relative_backgrounds)
    print('Output ROIs relative directory is:' + dir_relative_rois)

    # parameters
    enable_video_vis = 0
    fps = 23.976
    dt = 1/fps

    # looping every clip
    file_names = os.listdir(dir_relative_source)
    for file_name in file_names:
        print('Processing file:', file_name, ' ...')
        # file paths
        peds_csv_path_filtered = dir_relative_filtered_trajs + file_name[11:][:-4] + '_traj_ped_filtered.csv'
        vehs_csv_path_filtered = dir_relative_filtered_trajs + file_name[11:][:-4] + '_traj_veh_filtered.csv'
        roi_path = dir_relative_rois + file_name[11:][:-4] + "_roi"
        # checking file existence
        peds_csv_existed = os.path.isfile(peds_csv_path_filtered)
        vehs_csv_existed = os.path.isfile(vehs_csv_path_filtered)
        roi_existed = os.path.isfile(roi_path)
        if not (peds_csv_existed and vehs_csv_existed and roi_existed):
            sys.exit('Some recording files are missing, please check ...')
        # read roi
        roi_file = open(roi_path, 'rb')
        roi = pickle.load(roi_file)
        roi_file.close()

        # read csv files
        df_peds = pandas.read_csv(peds_csv_path_filtered)
        df_vehs = pandas.read_csv(vehs_csv_path_filtered)

        # obtain background
        background = generate_background(file_name=file_name,
                                         dir_relative_source=dir_relative_source,
                                         dir_relative_backgrounds=dir_relative_backgrounds,
                                         roi=roi,
                                         method='GSOC')

        # Plot pedestrian and vehicle trajectories
        plt.figure(1)
        plt.imshow(cv2.cvtColor(background, cv2.COLOR_BGR2RGB))
        id_peds = list(set(df_peds.id))
        id_vehs = list(set(df_vehs.id))
        for id_ped in id_peds:
            plt.plot(df_peds[df_peds.id == id_ped].x_est, df_peds[df_peds.id == id_ped].y_est)
        for id_veh in id_vehs:
            plt.plot(df_vehs[df_vehs.id == id_veh].x_est, df_vehs[df_vehs.id == id_veh].y_est, 'r--', lw=2)
        plt.axis([0, roi[2], 0, roi[3]])
        plt.gca().invert_yaxis()
        plt.show()

        # Video Visualization
        if enable_video_vis:
            video = cv2.VideoCapture(dir_relative_source + file_name)
            width = int(video.get(3))
            height = int(video.get(4))
            fps = video.get(5)
            print('Video size:', width, height, 'fps:', fps)

            frame_index = 0
            while True:

                # Read a new frame
                frame_ok, frame = video.read()
                if not frame_ok:
                    break
                frame_index = frame_index + 1

                if frame_index == 1:
                    # initialize video writers: roi + roi with tracking results
                    fourcc = cv2.VideoWriter_fourcc(*'XVID')
                    roi_width = roi[2]
                    roi_height = roi[3]
                    video_path_roi_clips = dir_relative_clipped + file_name[11:][:-4] + '_roi.mp4'
                    video_path_roi_clips_with_box = dir_relative_clipped + file_name[11:][:-4] + '_roi_box.mp4'

                    roi_video_out_existed = os.path.isfile(video_path_roi_clips)
                    roi_video_out_box_existed = os.path.isfile(video_path_roi_clips_with_box)

                    if not roi_video_out_existed:
                        video_roi_out = cv2.VideoWriter(video_path_roi_clips, fourcc, fps, (roi_width, roi_height))
                    if not roi_video_out_box_existed:
                        video_roi_out_box = cv2.VideoWriter(video_path_roi_clips_with_box, fourcc, fps, (roi_width, roi_height))

                # roi
                frame = frame[roi[1]:(roi[1]+roi[3]), roi[0]:(roi[0]+roi[2])]
                if not roi_video_out_existed:
                    video_roi_out.write(frame)

                # peds data
                frame_ped_data = df_peds[df_peds.frame == frame_index]
                id_peds_frame = list(frame_ped_data.id)
                for id_ped in id_peds_frame:
                    cv2.circle(frame,
                               (frame_ped_data[frame_ped_data.id == id_ped].x_est,
                                frame_ped_data[frame_ped_data.id == id_ped].y_est),
                               5, (255, 0, 0), 2)
                    cv2.putText(frame, str(id_ped),
                                (frame_ped_data[frame_ped_data.id == id_ped].x_est,
                                 frame_ped_data[frame_ped_data.id == id_ped].y_est),
                                cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)
                # vehs data
                frame_veh_data = df_vehs[df_vehs.frame == frame_index]
                id_vehs_frame = list(frame_veh_data.id)
                for id_veh in id_vehs_frame:
                    corners = []
                    cv2.circle(frame,
                               (frame_veh_data[frame_veh_data.id == id_veh].x_est,
                                frame_veh_data[frame_veh_data.id == id_veh].y_est),
                               3, (0, 0, 255), 2)
                    cv2.putText(frame, "veh " + str(id_veh),
                                (frame_veh_data[frame_veh_data.id == id_veh].x_est,
                                 frame_veh_data[frame_veh_data.id == id_veh].y_est),
                                cv2.FONT_HERSHEY_DUPLEX, 0.5, (0, 255, 0), 1)
                    # corners.append((frame_veh_data[frame_veh_data.id == id_veh].x_fl, frame_veh_data[frame_veh_data.id == id_veh].y_fl))
                    # corners.append((frame_veh_data[frame_veh_data.id == id_veh].x_fr, frame_veh_data[frame_veh_data.id == id_veh].y_fr))
                    # corners.append((frame_veh_data[frame_veh_data.id == id_veh].x_rr, frame_veh_data[frame_veh_data.id == id_veh].y_rr))
                    # corners.append((frame_veh_data[frame_veh_data.id == id_veh].x_rl, frame_veh_data[frame_veh_data.id == id_veh].y_rl))
                    # cv2.line(frame, corners[0], corners[1], (0, 255, 0), 1)
                    # cv2.line(frame, corners[1], corners[2], (0, 255, 0), 1)
                    # cv2.line(frame, corners[2], corners[3], (0, 255, 0), 1)
                    # cv2.line(frame, corners[3], corners[0], (0, 255, 0), 1)

                # write video roi out with box
                if not roi_video_out_box_existed:
                    video_roi_out_box.write(frame)

                # imshow
                cv2.imshow('Recorded Trajectories', frame)
                k = cv2.waitKey(1) & 0xff
                if k == 27:  # 'ESC'
                    break

            if not roi_video_out_existed:
                video_roi_out.release()
            if not roi_video_out_box_existed:
                video_roi_out_box.release()
