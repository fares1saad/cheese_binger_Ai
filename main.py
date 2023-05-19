import matplotlib.pyplot as plt

# The time taken by the alpha-beta algorithm for each move
alpha_beta_times = [0.8235933780670166, 0.8570008277893066, 0.9179973602294922, 0.3269999027252197, 0.5880000591278076, 0.6869964599609375, 0.4036428928375244, 0.24799823760986328, 0.26900267601013184, 0.14800071716308594, 0.12299871444702148, 0.06599998474121094, 0.03500223159790039, 0.048000335693359375, 0.011998653411865234, 0.0069997310638427734, 0.00500035285949707, 0.003000020980834961, 0.0009975433349609375, 0.0010020732879638672]

# The time taken by the minmax algorithm for each move
minmax_times = [5.48799729347229, 5.480998516082764, 5.2030029296875, 4.982001543045044, 4.8929994106292725, 4.608999967575073, 2.164999008178711, 2.111999988555908, 1.7329905033111572, 0.898998498916626, 0.7880001068115234, 0.2690002918243408, 0.1999988555908203, 0.16299891471862793, 0.0330049991607666, 0.037999629974365234, 0.011000871658325195, 0.004995822906494141, 0.0020034313201904297, 0.0009999275207519531]

# Create a list of move numbers for the x-axis
moves = list(range(1, len(alpha_beta_times)+1))

# Create a figure and axis object
fig, ax = plt.subplots()

# Plot the alpha-beta times as a blue line
ax.plot(moves, alpha_beta_times, color='blue', label='Alpha-Beta')

# Plot the minmax times as a red line
ax.plot(moves, minmax_times, color='red', label='Minmax')

# Set the axislabels and title
ax.set_xlabel('Move Number')
ax.set_ylabel('Time (seconds)')
ax.set_title('Comparison of Alpha-Beta and Minmax Algorithms')

# Add a legend to the plot
ax.legend()

# Show the plot
plt.show()