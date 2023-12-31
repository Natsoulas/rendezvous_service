"""The file where the visualizations live."""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read history df from csv.
# dtype_mapping = {
#     'Time History': np.object,  # Use np.object for arrays or mixed types
#     'Helper State History': np.object,
#     'Target State History': np.object,
#     'Thruster History': np.object,
#     'Relative Distance History': np.float64,  # Specify the correct data types for non-array columns
#     'Relative Speed History': np.float64,
# }
history_df = pd.read_json('sim_trial.json')
# Grab postion vectors from both the helper and target.

x_h_hist = history_df['x_helper_history'].values
# Make a relative distance (magnitude) vs time plot.
# Concatenate the arrays along the second axis to form a single (1000, 3) array
relative_dist_history = np.concatenate((np.reshape(history_df['dist_x_history'].values, (len(history_df['dist_x_history'].values),1)), np.reshape(history_df['dist_y_history'].values, (len(history_df['dist_x_history'].values),1)), np.reshape(history_df['dist_z_history'].values, (len(history_df['dist_x_history'].values),1))), axis=1)
# Calculate the magnitude for each row
dist_magnitude = np.linalg.norm(relative_dist_history, axis=1).reshape(-1, 1)

plot1 = plt.figure(1)
plt.plot(history_df['Time History'].values, dist_magnitude)
plt.title("Relative distance between satellites vs. time")
plt.xlabel("time (s)")
plt.ylabel("Magnitude of relative distance")

print(np.min(dist_magnitude))
print(history_df['Time History'].values[np.argmin(dist_magnitude)])
# Make a 3d plot of both satellites' trajectories over the course of the whole simulation.

plot3 = plt.figure(3)
ax = plt.axes(projection='3d')
# Data for a three-dimensional plot
ax.scatter3D(history_df['x_helper_history'].values, history_df['y_helper_history'].values, history_df['z_helper_history'].values, 'red')
ax.scatter3D(history_df['x_target_history'].values, history_df['y_target_history'].values, history_df['z_target_history'].values, 'gray')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

# Control Thrust History Plots

u_history = np.concatenate((np.reshape(history_df['Ux History'].values, (len(history_df['Ux History'].values),1)), np.reshape(history_df['Uy History'].values, (len(history_df['Ux History'].values),1)), np.reshape(history_df['Uz History'].values, (len(history_df['Ux History'].values),1))), axis=1)
# Calculate the magnitude for each row
u_magnitude = np.linalg.norm(u_history, axis=1).reshape(-1, 1)

plot2 = plt.figure(2)
plt.plot(history_df['Time History'].values, u_magnitude)
plt.title("Magnitude of Control Thrust vs. time")
plt.xlabel("time (s)")
plt.ylabel("Magnitude of Control Thrust Force (N)")

plot4 = plt.figure(4)
plt.plot(history_df['Time History'].values, np.reshape(history_df['Ux History'].values, (len(history_df['Ux History'].values))))
plt.title("Magnitude of Control Thrust in x direction vs. time")
plt.xlabel("time (s)")
plt.ylabel("Magnitude of x-direction Control Thrust Force (N)")

plot5 = plt.figure(5)
plt.plot(history_df['Time History'].values, np.reshape(history_df['Uy History'].values, (len(history_df['Uy History'].values))))
plt.title("Magnitude of Control Thrust in y direction vs. time")
plt.xlabel("time (s)")
plt.ylabel("Magnitude of y-direction Control Thrust Force (N)")

plot10 = plt.figure(10)
plt.plot(history_df['Time History'].values, np.reshape(history_df['Uz History'].values, (len(history_df['Uz History'].values))))
plt.title("Magnitude of Control Thrust in z direction vs. time")
plt.xlabel("time (s)")
plt.ylabel("Magnitude of z-direction Control Thrust Force (N)")

# Relative Distance Component Plots
plot6 = plt.figure(6)
plt.plot(history_df['Time History'].values, np.reshape(history_df['dist_x_history'].values, (len(history_df['dist_x_history'].values))))
plt.title("Magnitude of Relative Distance between satellites in x direction vs. time")
plt.xlabel("time (s)")
plt.ylabel("Magnitude of x-direction distance (m)")

plot7 = plt.figure(7)
plt.plot(history_df['Time History'].values, np.reshape(history_df['dist_y_history'].values, (len(history_df['dist_y_history'].values))))
plt.title("Magnitude of Relative Distance between satellites in y direction vs. time")
plt.xlabel("time (s)")
plt.ylabel("Magnitude of y-direction distance (m)")

plot8 = plt.figure(8)
plt.plot(history_df['Time History'].values, np.reshape(history_df['dist_z_history'].values, (len(history_df['dist_z_history'].values))))
plt.title("Magnitude of Relative Distance between satellites in z direction vs. time")
plt.xlabel("time (s)")
plt.ylabel("Magnitude of z-direction distance (m)")