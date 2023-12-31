"""The file where the rendezvous simulation architecture lives."""

import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import constants as c 
from tools import kepler2rv
from dynamics import target_satellite_eom, integrate_states_forward
from controls import orbit_controller

# Start by setting up initial conditions.
r_helper_initial, v_helper_initial = kepler2rv(c.a*1000,c.e, np.deg2rad(c.raan), np.deg2rad(c.i),0,0,c.mu_earth)
r_target_initial, v_target_initial = kepler2rv(c.a_t*1000,c.e_t, np.deg2rad(c.raan_t), np.deg2rad(c.i_t),0,0,c.mu_earth)

# Set up convergence criteria
r_conv_criteria = 10 # Relative distance must be less than 10 meters.
v_conv_criteria = 0.1 # Difference in velocities should be less than 0.1 m/s in magnitude.
conv_criteria = [r_conv_criteria, v_conv_criteria]

# Define actual rendezvous simulation function:
def run_rendezvous_sim(z_init_helper, z_init_target, conv_criteria):
    # Initialize parameters.
    converged = False
    z_helper = z_init_helper
    z_target = z_init_target
    F_control = np.array([0,0,0])
    rel_distance = z_helper[:3] - z_target[:3]
    rel_speed_diff = z_helper[3:6] - z_target[3:6]
    t = 0
    iter_count = 1
    # Initialize Histories for saving simulation data.
    t_history = [t]
    z_helper_history = np.array([z_helper])
    z_target_history = np.array([z_target])
    F_control_history = np.array([F_control])
    rel_distance_history = np.array([rel_distance])
    rel_speed_diff_history = np.array([rel_speed_diff])
    # Control loop that exits when converged.
    while not converged and t < int(6E5):
        # Input state to controller.
        F_control, rel_distance, rel_speed_diff, A, B = orbit_controller(np.concatenate((z_helper,z_target)), F_control, c.m)
        # Input Control Thrust and both helper and target states to dynamics.
        # Integrate dynamics to propagate forward 1 second.
        seconds_forward = 100
        z_helper_scipy, z_target_scipy = integrate_states_forward(z_helper, z_target, F_control, seconds_forward)
        z_helper = z_helper_scipy.y.flatten()
        z_target = z_target_scipy.y.flatten()
        # Increment to new time (add one second).
        t += seconds_forward
        # Append newest data to respective history arrrays: (hopefully .append() works for np arrays and all.)
        t_history.append(t)
        z_helper_history = np.append(z_helper_history,np.reshape(z_helper,(1,6)),0)
        z_target_history = np.append(z_target_history,np.reshape(z_target,(1,6)),0)
        F_control_history = np.append(F_control_history,np.reshape(F_control,(1,3)),0)
        rel_distance_history = np.append(rel_distance_history,np.reshape(rel_distance,(1,3)),0)
        rel_speed_diff_history = np.append(rel_speed_diff_history,np.reshape(rel_speed_diff,(1,3)),0)
        # Check for convergence.
        if conv_criteria[0] > np.linalg.norm(rel_distance) and conv_criteria[1] > np.linalg.norm(rel_speed_diff):
            converged = True
        iter_count += 1
    return t_history, z_helper_history, z_target_history, F_control_history, rel_distance_history, rel_speed_diff_history