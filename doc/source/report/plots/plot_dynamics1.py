from mousestyles.data import load_time_matrix_dynamics
from mousestyles.visualization.dynamics import plot_dynamics


time_matrix = load_time_matrix_dynamics()
plot_dynamics(time_matrix, 1)
