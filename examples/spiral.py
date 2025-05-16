import os
import csv
from copy import copy
import numpy as np

from ruckig import InputParameter, OutputParameter, Result, Ruckig
from splitter import split_csv


if __name__ == '__main__':
    # Create instances: the Ruckig OTG as well as input and output parameters
    fs = 5e3
    Ts = 1/fs
    otg = Ruckig(2, Ts)  # DoFs, control cycle
    inp = InputParameter(2)
    out = OutputParameter(2)
    enc_res = 10e6
    # Set input parameters       r  , theta
    inp.current_position =      [2.5, 4*np.pi] # mm, rad
    inp.current_velocity =      [0.0, 0.0]
    inp.current_acceleration =  [0.0, 0.0]

    inp.target_position         = [0.0, 0.0] # mm, rad
    inp.target_velocity         = [0.0, 0.0]
    inp.target_acceleration     = [0.0, 0.0]

    inp.max_velocity = [0.1, 0.4*np.pi]
    # inp.max_acceleration = [0.06, 0.1*np.pi]
    # inp.max_jerk = [0.06, 0.1*np.pi]
#####################################

    # Generate the trajectory within the control loop
    first_output, out_list = None, []
    res = Result.Working

    # Initialize the file and writer
    dir_path = "./output/data"
    os.makedirs(dir_path, exist_ok=True)
    filename="output.csv"
    cartesian_positions=[]
    cartesian_velocities=[]
    cartesian_accelerations=[]
    with open(os.path.join(dir_path, filename), 'w', newline='') as file:
        writer = csv.writer(file)

        while res == Result.Working:
            res = otg.update(inp, out)

            r        = out.new_position[0]
            theta    = out.new_position[1]
            dr       = out.new_velocity[0]
            dtheta   = out.new_velocity[1]
            ddr      = out.new_acceleration[0]
            ddtheta  = out.new_acceleration[1]

            x   = enc_res * (r * np.cos(theta))
            dx  = enc_res * (dr * np.cos(theta) - r * dtheta * np.sin(theta))
            ddx = enc_res * (((ddr * np.cos(theta)) - (dr * dtheta * np.sin(theta))) - ((dr * dtheta + r * ddtheta) * np.sin(theta) + (r * dtheta * dtheta * np.cos(theta))))

            y   = enc_res*(r * np.sin(theta))
            dy  = enc_res*(dr * np.sin(theta) + r * dtheta * np.cos(theta))
            ddy = enc_res*(((ddr * np.sin(theta)) + (dr * dtheta * np.cos(theta))) + ((dr * dtheta + r * ddtheta) * np.cos(theta) - (r * dtheta * dtheta * np.sin(theta))))

            writer.writerow([int(x), int(y)])
            cartesian_positions.append([x, y])
            cartesian_velocities.append([dx, dy])
            cartesian_accelerations.append([ddx, ddy])

            out_list.append(copy(out))
            out.pass_to_input(inp)

            if not first_output:
                first_output = copy(out)

    print(f"Data written to {filename}")
    print(f'Calculation duration: {first_output.calculation_duration:0.1f} [µs]')
    print(f'Trajectory duration: {first_output.trajectory.duration:0.6f} [s]')


    # Save the trajectory into a file
    from pathlib import Path
    # TODO

    split_csv(dir_path, filename, lines_per_file=10000)

    # Plot the trajectory
    from plotter import Plotter

    project_path = Path(__file__).parent.parent.absolute()

    Plotter.plot_trajectory(project_path / 'examples' / '01-x_trajectory.pdf', otg, inp, out_list, plot_acceleration=True, plot_jerk=True, show=True)
    Plotter.plot_cartesian(cartesian_positions)
    Plotter.plot_cart_traj(out_list, otg.delta_time, cartesian_positions, cartesian_velocities, cartesian_accelerations, True)
    import matplotlib.pyplot as plt
    plt.show()