import os
import pandas
import cv2
import matplotlib.pyplot as plt
import numpy as np
import datetime

from tools.kalman_filters import LinearPointMass, NonlinearKinematicBicycle


def get_scenarios_names(data_dir):
    file_names = os.listdir(data_dir)
    scenarios = [file_name[:-13] for file_name in file_names]
    scenarios = list(set(scenarios))
    scenarios.sort(reverse=False)
    return scenarios


def main():

    # dirs
    dir_trajs = '../data/trajectories/'
    dir_trajs_filtered = '../data/trajectories_filtered/'
    dir_backgrounds = '../data/backgrounds/'
    dir_ratios = '../data/ratios/'
    dir_figures = '../data/figures/'

    # params
    fps = 23.976
    dt = 1/fps

    pandas.set_option('display.max_columns', 15)

    # initialize Kalman filters
    filter_ped = LinearPointMass(dt=dt)
    filter_veh = NonlinearKinematicBicycle(lf=1.2, lr=1.0, dt=dt)

    # process each file (data)
    scenarios = get_scenarios_names(dir_trajs)
    for scenario in scenarios:
        print('processing', scenario, '...')
        background = cv2.imread(dir_backgrounds + scenario + '_background_GSOC.png')

        # load trajs
        df_peds = pandas.read_csv(dir_trajs + scenario + '_traj_ped.csv')
        df_vehs = pandas.read_csv(dir_trajs + scenario + '_traj_veh.csv')

        # ratio - convert to meters
        ratio = float(np.loadtxt(dir_ratios + scenario + '_ratio_pixel2meter.txt'))
        df_peds.x = df_peds.x/ratio
        df_peds.y = df_peds.y/ratio
        # df_vehs = df_vehs[['id', 'x_c', 'y_c', 'frame', 'label']]
        df_vehs.x_c = df_vehs.x_c/ratio
        df_vehs.y_c = df_vehs.y_c/ratio

        # vis
        plt.figure(1)
        plt.imshow(cv2.cvtColor(background, cv2.COLOR_BGR2RGB))

        # ids
        id_peds = list(set(df_peds.id))
        id_vehs = list(set(df_vehs.id))
        for id_ped in id_peds:

            print('filtering trajectory of pedestrian ', id_ped, '...')

            # individual ped traj
            df_ped = df_peds[df_peds.id == id_ped]
            # plot orginal
            plt.plot(df_ped.x*ratio, df_ped.y*ratio)

            id_frames = list(df_peds[df_peds.id == id_ped].frame)
            for i, id_frame in enumerate(id_frames): # id_frame: index of the frame
                # print('now at frame:', id_frame)
                id_dataframe = int(df_ped[df_ped.frame == id_frame].index.values)
                if i == 0: # initalize KF
                    df_peds.loc[id_dataframe, 'x_est'] = float(df_peds.loc[id_dataframe, 'x'])
                    df_peds.loc[id_dataframe, 'vx_est'] = (float(df_ped[df_ped.frame == id_frame + 1].x)
                                                    - float(df_ped[df_ped.frame == id_frame].x)) / (1*dt)
                    df_peds.loc[id_dataframe, 'y_est'] = float(df_peds.loc[id_dataframe, 'y'])
                    df_peds.loc[id_dataframe, 'vy_est'] = (float(df_ped[df_ped.frame == id_frame + 1].y)
                                                    - float(df_ped[df_ped.frame == id_frame].y)) / (1*dt)
                    P_matrix = np.identity(4)
                elif i < len(id_frames):
                    # assign new est values
                    df_peds.loc[id_dataframe, 'x_est'] = x_vec_est_new[0][0]
                    df_peds.loc[id_dataframe, 'vx_est'] = x_vec_est_new[1][0]
                    df_peds.loc[id_dataframe, 'y_est'] = x_vec_est_new[2][0]
                    df_peds.loc[id_dataframe, 'vy_est'] = x_vec_est_new[3][0]

                if i < len(id_frames)-1: # no action on last data
                    # filtering
                    x_vec_est = np.array([[df_peds.loc[id_dataframe].x_est],
                                          [df_peds.loc[id_dataframe].vx_est],
                                          [df_peds.loc[id_dataframe].y_est],
                                          [df_peds.loc[id_dataframe].vy_est]])
                    z_new = np.array([[float(df_ped[df_ped.frame == id_frame+1].x)],
                                      [float(df_ped[df_ped.frame == id_frame+1].y)]])
                    x_vec_est_new, P_matrix_new = filter_ped.predict_and_update(
                        x_vec_est=x_vec_est,
                        u_vec=np.array([[0.], [0.]]),
                        P_matrix=P_matrix,
                        z_new=z_new
                    )
                    P_matrix = P_matrix_new

            # plot filtered
            plt.plot(df_peds[df_peds.id == id_ped].x_est*ratio, df_peds[df_peds.id == id_ped].y_est*ratio, 'k', lw=1)

        for id_veh in id_vehs:

            print('filtering trajectory of vehicle ', id_veh, '...')
            df_veh = df_vehs[df_vehs.id == id_veh]
            # plot orginal
            plt.plot(df_veh.x_c*ratio, df_veh.y_c*ratio, 'r--', lw=2)

            df_veh_frames = list(df_vehs[df_vehs.id == id_veh].frame)

            # loop each frame
            for i, id_frame in enumerate(df_veh_frames):
                # print('now at id:', id_frame)
                id_dataframe = int(df_veh[df_veh.frame == id_frame].index.values)
                if i == 0:  # initalize KF

                    # initial x, y
                    df_vehs.loc[id_dataframe, 'x_est'] = float(df_vehs.loc[id_dataframe, 'x_c'])
                    df_vehs.loc[id_dataframe, 'y_est'] = float(df_vehs.loc[id_dataframe, 'y_c'])

                    # estimating initial velocity
                    if len(df_veh_frames) < 11: # increment for estimating initial velocity
                        increment = len(df_veh_frames) - 1
                    else:
                        increment = 10
                    vx = (float(df_veh[df_veh.frame == id_frame + increment].x_c)
                          - float(df_veh[df_veh.frame == id_frame].x_c)) / (increment * dt)
                    vy = (float(df_veh[df_veh.frame == id_frame + increment].y_c)
                          - float(df_veh[df_veh.frame == id_frame].y_c)) / (increment * dt)
                    df_vehs.loc[id_dataframe, 'vel_est'] = np.linalg.norm([[vx], [vy]])
                    print('initial velocity:', np.linalg.norm([[vx], [vy]]))

                    # estimating initial heading angle
                    fl = np.array([[df_vehs.loc[id_dataframe, 'x_fl']], [df_vehs.loc[id_dataframe, 'y_fl']]])/ratio
                    fr = np.array([[df_vehs.loc[id_dataframe, 'x_fr']], [df_vehs.loc[id_dataframe, 'y_fr']]])/ratio
                    rl = np.array([[df_vehs.loc[id_dataframe, 'x_rl']], [df_vehs.loc[id_dataframe, 'y_rl']]])/ratio
                    rr = np.array([[df_vehs.loc[id_dataframe, 'x_rr']], [df_vehs.loc[id_dataframe, 'y_rr']]])/ratio
                    vec_heading = (fl + fr)/2 - (rl + rr)/2
                    df_vehs.loc[id_dataframe, 'psi_est'] = np.arctan2(vec_heading[1][0], vec_heading[0][0])
                    print('initial heading angle:', np.arctan2(vy, vx), np.arctan2(vec_heading[1][0], vec_heading[0][0]))
                    # df_vehs.loc[id_dataframe, 'psi_est'] = np.arctan2(vy, vx)

                    # initial P_matrix
                    P_matrix = np.identity(4)
                elif i < len(df_veh_frames):
                    # assign new est values
                    df_vehs.loc[id_dataframe, 'x_est'] = x_vec_est_new[0][0]
                    df_vehs.loc[id_dataframe, 'y_est'] = x_vec_est_new[1][0]
                    df_vehs.loc[id_dataframe, 'psi_est'] = x_vec_est_new[2][0]
                    df_vehs.loc[id_dataframe, 'vel_est'] = x_vec_est_new[3][0]

                if i < len(df_veh_frames) - 1:  # no action on last data
                    # filtering
                    x_vec_est = np.array([[df_vehs.loc[id_dataframe].x_est],
                                          [df_vehs.loc[id_dataframe].y_est],
                                          [df_vehs.loc[id_dataframe].psi_est],
                                          [df_vehs.loc[id_dataframe].vel_est]])
                    z_new = np.array([[float(df_veh[df_veh.frame == id_frame + 1].x_c)],
                                      [float(df_veh[df_veh.frame == id_frame + 1].y_c)]])
                    x_vec_est_new, P_matrix_new = filter_veh.predict_and_update(
                        x_vec_est=x_vec_est,
                        u_vec=np.array([[0.], [0.]]),
                        P_matrix=P_matrix,
                        z_new=z_new
                    )
                    P_matrix = P_matrix_new

            plt.plot(df_vehs[df_vehs.id == id_veh].x_est*ratio, df_vehs[df_vehs.id == id_veh].y_est*ratio, 'k', lw=2)

        # get time
        time = datetime.datetime.now()
        current_time = str(time.strftime(" %Y-%m-%d %H-%M-%S"))

        # save traj plot
        if not os.path.isdir(dir_figures):
            os.mkdir(dir_figures)
        if os.path.isfile(dir_figures + scenario + '_traj_plot.pdf'):
            plt.savefig(dir_figures + scenario + '_traj_plot' + current_time + '.pdf', bbox_inches='tight')
        else:
            plt.savefig(dir_figures + scenario + '_traj_plot.pdf', bbox_inches='tight')
        plt.clf()

        # write csv files
        if not os.path.isdir(dir_trajs_filtered):
            os.mkdir(dir_trajs_filtered)
        # write ped csv
        df_peds = df_peds[['id', 'frame', 'label', 'x_est', 'y_est', 'vx_est', 'vy_est']]
        if os.path.isfile(dir_trajs_filtered + scenario + '_traj_ped_filtered.csv'):
            print('ped traj file existed, current time is appended to the file name ...')
            df_peds.to_csv(dir_trajs_filtered + scenario + '_traj_ped_filtered' + current_time + '.csv', index=False)
        else:
            df_peds.to_csv(dir_trajs_filtered + scenario + '_traj_ped_filtered.csv', index=False)
        # write veh csv
        df_vehs = df_vehs[['id', 'frame', 'label', 'x_est', 'y_est', 'psi_est', 'vel_est']]
        if os.path.isfile(dir_trajs_filtered + scenario + '_traj_veh_filtered.csv'):
            print('veh traj file existed, current time is appended to the file name ...')
            df_vehs.to_csv(dir_trajs_filtered + scenario + '_traj_veh_filtered' + current_time + '.csv', index=False)
        else:
            df_vehs.to_csv(dir_trajs_filtered + scenario + '_traj_veh_filtered.csv', index=False)


if __name__ == '__main__':
    main()
