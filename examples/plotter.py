from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


class Plotter:
    @staticmethod
    def plot_trajectory(filename, otg, inp, out_list, show=False, plot_acceleration=True, plot_jerk=True, time_offsets=None, title=None):
        taxis = np.array(list(map(lambda x: x.time, out_list)))
        if time_offsets:
            taxis += np.array(time_offsets)
        qaxis = np.array(list(map(lambda x: x.new_position, out_list)))
        dqaxis = np.array(list(map(lambda x: x.new_velocity, out_list)))
        ddqaxis = np.array(list(map(lambda x: x.new_acceleration, out_list)))
        dddqaxis = np.diff(ddqaxis, axis=0, prepend=ddqaxis[0, 0]) / otg.delta_time
        dddqaxis[0, :] = 0.0
        dddqaxis[-1, :] = 0.0

        plt.figure(figsize=(8.0, 2.0 + 3.0 * inp.degrees_of_freedom), dpi=120)
        plt.subplot(inp.degrees_of_freedom, 1, 1)

        if title:
            plt.title(title)

        for dof in range(inp.degrees_of_freedom):
            global_max = np.max([qaxis[:, dof], dqaxis[:, dof], ddqaxis[:, dof]])
            global_min = np.min([qaxis[:, dof], dqaxis[:, dof], ddqaxis[:, dof]])

            if plot_jerk:
                global_max = max(global_max, np.max(dddqaxis[:, dof]))
                global_min = min(global_min, np.min(dddqaxis[:, dof]))

            plt.subplot(inp.degrees_of_freedom, 1, dof + 1)
            plt.ylabel(f'DoF {dof + 1}')
            plt.plot(taxis, qaxis[:, dof], label=f'Position {dof + 1}')
            plt.plot(taxis, dqaxis[:, dof], label=f'Velocity {dof + 1}')
            if plot_acceleration:
                plt.plot(taxis, ddqaxis[:, dof], label=f'Acceleration {dof + 1}')
            if plot_jerk:
                plt.plot(taxis, dddqaxis[:, dof], label=f'Jerk {dof + 1}')

            # Plot sections
            if hasattr(out_list[-1], 'trajectory'):
                linewidth = 1.0 if len(out_list[-1].trajectory.intermediate_durations) < 20 else 0.25
                for t in out_list[-1].trajectory.intermediate_durations:
                    plt.axvline(x=t, color='black', linestyle='--', linewidth=linewidth)

            # Plot limit lines
            if inp.min_position and inp.min_position[dof] > 1.4 * global_min:
                plt.axhline(y=inp.min_position[dof], color='grey', linestyle='--', linewidth=1.1)

            if inp.max_position and inp.max_position[dof] < 1.4 * global_max:
                plt.axhline(y=inp.max_position[dof], color='grey', linestyle='--', linewidth=1.1)

            if inp.max_velocity[dof] < 1.4 * global_max:
                plt.axhline(y=inp.max_velocity[dof], color='orange', linestyle='--', linewidth=1.1)

            min_velocity = inp.min_velocity[dof] if inp.min_velocity else -inp.max_velocity[dof]
            if min_velocity > 1.4 * global_min:
                plt.axhline(y=min_velocity, color='orange', linestyle='--', linewidth=1.1)

            if plot_acceleration and inp.max_acceleration[dof] < 1.4 * global_max:
                plt.axhline(y=inp.max_acceleration[dof], color='g', linestyle='--', linewidth=1.1)

            min_acceleration = inp.min_acceleration[dof] if inp.min_acceleration else -inp.max_acceleration[dof]
            if plot_acceleration and min_acceleration > 1.4 * global_min:
                plt.axhline(y=min_acceleration, color='g', linestyle='--', linewidth=1.1)

            if plot_jerk and inp.max_jerk[dof] < 1.4 * global_max:
                plt.axhline(y=inp.max_jerk[dof], color='red', linestyle='--', linewidth=1.1)

            if plot_jerk and -inp.max_jerk[dof] > 1.4 * global_min:
                plt.axhline(y=-inp.max_jerk[dof], color='red', linestyle='--', linewidth=1.1)

            plt.legend()
            plt.grid(True)

        plt.xlabel('t')
        plt.savefig(Path(__file__).parent.parent / 'build' / filename)

        # if show:
        #     plt.show()


    @staticmethod
    def plot_DoFPositions(inp, out_list):
        qaxis = np.array(list(map(lambda x: x.new_position, out_list)))
        if inp.degrees_of_freedom == 2:
            xaxis = qaxis[:,0]
            yaxis = qaxis[:,1]
            plt.figure(figsize=(8.0, 5.0), dpi=120)
            #plt.subplot(inp.degrees_of_freedom, 1, 1)
            plt.plot(xaxis, yaxis,'o')
            # plt.show()
        elif inp.degrees_of_freedom == 3:
            xaxis = qaxis[:,0]
            yaxis = qaxis[:,1]
            zaxis = qaxis[:,2]

            #ax = plt.figure(figsize=(8.0, 5.0), dpi=120, projection='3d')
            #plt.subplot(inp.degrees_of_freedom, 1, 1)
            plt.plot(xaxis, yaxis,zaxis,marker='o')


    def plot_2DoF(out_list,setpoints=None,pltPos=True,pltVel=False,pltAcc=False, velSize=1.0, accSize=1.0):
        qaxis = np.array(list(map(lambda x:   x.new_position, out_list)))
        dqaxis = np.array(list(map(lambda x:  x.new_velocity, out_list)))
        ddqaxis = np.array(list(map(lambda x: x.new_acceleration, out_list)))
        # dddqaxis = np.diff(ddqaxis, axis=0, prepend=ddqaxis[0, 0]) / otg.delta_time
        # dddqaxis[0, :] = 0.0
        # dddqaxis[-1, :] = 0.0

        px = qaxis[:,0]
        py = qaxis[:,1]
        vx = dqaxis[:,0]
        vy = dqaxis[:,1]
        ax = ddqaxis[:,0]
        ay = ddqaxis[:,1]
        # jx = dddqaxis[:,0]
        # jy = dddqaxis[:,1]

        plt.figure(figsize=(8.0, 5.0), dpi=120)

        if pltAcc:
            # acceleration_colors = ["#cc000050", "#e6913850"]
            acceleration_colors = ["#2ca02c50"]
            for i in range(1, len(ax) - 1):
                plt.plot(
                [px[i], px[i] + ax[i] * accSize],
                [py[i], py[i] + ay[i] * accSize],
                color=acceleration_colors[i % len(acceleration_colors)],
                )

        if pltVel:
            # velocity_colors = ["#a64d7950","#674ea750"]
            velocity_colors = ["#ff7f0e50"]
            for i in range(1, len(vx) - 1):
                plt.plot(
                [px[i], px[i] + vx[i] * velSize],
                [py[i], py[i] + vy[i] * velSize],
                color=velocity_colors[i % len(velocity_colors)],
                )
        if pltPos:
            plt.plot(px,py,marker='.',linestyle='')

        # for i in range(out_list.getEndSize()):
        #     sp=setpoints.getEndPos(i)
        #     plt.plot(sp[0],sp[1],marker='o',color='r',linestyle='')


        # plt.show()
        # plt.savefig('1-x.png')


    @staticmethod
    def plot_cart_traj(out_list, delta_time, positions, velocities = None, acceleration = None, plot_jerk=False):
        taxis = np.array(list(map(lambda x: x.time, out_list)))

        qaxis    = np.array(positions)
        dqaxis   = np.array(velocities)
        ddqaxis  = np.array(acceleration)
        dddqaxis = np.diff(ddqaxis, axis=0, prepend=ddqaxis[0, 0]) / delta_time
        dddqaxis[0, :] = 0.0
        dddqaxis[-1, :] = 0.0

        plt.figure(figsize=(8.0, 2.0 + 3.0 * 2), dpi=120)
        plt.subplot(2, 1, 1)

        for dof in range(2):
            global_max = np.max([qaxis[:, dof], dqaxis[:, dof], ddqaxis[:, dof]])
            global_min = np.min([qaxis[:, dof], dqaxis[:, dof], ddqaxis[:, dof]])

            global_max = max(global_max, np.max(dddqaxis[:, dof]))
            global_min = min(global_min, np.min(dddqaxis[:, dof]))

            plt.subplot(2, 1, dof + 1)
            plt.ylabel(f'DoF {dof + 1}')
            plt.plot(taxis, qaxis[:, dof], label=f'Position {dof + 1}')
            plt.plot(taxis, dqaxis[:, dof], label=f'Velocity {dof + 1}')
            if acceleration:
                plt.plot(taxis, ddqaxis[:, dof], label=f'Acceleration {dof + 1}')
                if plot_jerk:
                    plt.plot(taxis, dddqaxis[:, dof], label=f'Jerk {dof + 1}')

            # Plot sections
            if hasattr(out_list[-1], 'trajectory'):
                linewidth = 1.0 if len(out_list[-1].trajectory.intermediate_durations) < 20 else 0.25
                for t in out_list[-1].trajectory.intermediate_durations:
                    plt.axvline(x=t, color='black', linestyle='--', linewidth=linewidth)

            # # Plot limit lines
            # if inp.min_position and inp.min_position[dof] > 1.4 * global_min:
            #     plt.axhline(y=inp.min_position[dof], color='grey', linestyle='--', linewidth=1.1)

            # if inp.max_position and inp.max_position[dof] < 1.4 * global_max:
            #     plt.axhline(y=inp.max_position[dof], color='grey', linestyle='--', linewidth=1.1)

            # if inp.max_velocity[dof] < 1.4 * global_max:
            #     plt.axhline(y=inp.max_velocity[dof], color='orange', linestyle='--', linewidth=1.1)

            # min_velocity = inp.min_velocity[dof] if inp.min_velocity else -inp.max_velocity[dof]
            # if min_velocity > 1.4 * global_min:
            #     plt.axhline(y=min_velocity, color='orange', linestyle='--', linewidth=1.1)

            # if plot_acceleration and inp.max_acceleration[dof] < 1.4 * global_max:
            #     plt.axhline(y=inp.max_acceleration[dof], color='g', linestyle='--', linewidth=1.1)

            # min_acceleration = inp.min_acceleration[dof] if inp.min_acceleration else -inp.max_acceleration[dof]
            # if plot_acceleration and min_acceleration > 1.4 * global_min:
            #     plt.axhline(y=min_acceleration, color='g', linestyle='--', linewidth=1.1)

            # if plot_jerk and inp.max_jerk[dof] < 1.4 * global_max:
            #     plt.axhline(y=inp.max_jerk[dof], color='red', linestyle='--', linewidth=1.1)

            # if plot_jerk and -inp.max_jerk[dof] > 1.4 * global_min:
            #     plt.axhline(y=-inp.max_jerk[dof], color='red', linestyle='--', linewidth=1.1)

            plt.legend()
            plt.grid(True)

        plt.xlabel('t')
        # plt.savefig(Path(__file__).parent.parent / 'build' / filename)
        # if show:

    @staticmethod
    def plot_cartesian(position_array):
        qaxis = np.array(position_array)
        xaxis = qaxis[:, 0]
        yaxis = qaxis[:, 1]
        plt.figure(figsize=(8.0, 5.0), dpi=120)
        plt.plot(xaxis, yaxis, marker='.')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Cartesian Trajectory (Spiral)')
        plt.grid(True)
        plt.savefig('spiral_cartesian.png')
