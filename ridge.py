import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.ticker import MaxNLocator

# Load the dataset
file_path = 'data.csv'  # Replace with your CSV file path
data = pd.read_csv(file_path)

# Convert 'Time' column to datetime to extract hour information
data['Time'] = pd.to_datetime(data['Time'])
data['Hour'] = data['Time'].dt.hour

# Group the data by 'Day', 'Hour', and 'Gym' locations to calculate the average attendance
average_attendance = data.groupby(['Day', 'Hour'])[['GymA', 'GymB', 'GymC']].mean().reset_index()

# Define the order of the days
ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Function to create filled line plots
def create_filled_line_plots_with_hours(gym_data, gym_name):
    # Set the color palette
    palette = sns.color_palette("coolwarm", 7)

    # Create subplots for each day with shared x and y axis
    fig, axes = plt.subplots(7, 1, figsize=(12, 14), sharex=True, sharey=True)

    # Plot for each day
    for i, day in enumerate(ordered_days):
        ax = axes[i]
        day_data = gym_data[gym_data['Day'] == day]
        # Generate the line plot and fill under the curve
        sns.lineplot(data=day_data, x='Hour', y=gym_name, ax=ax, legend=False, color=palette[i])
        ax.fill_between(day_data['Hour'], day_data[gym_name], alpha=0.3, color=palette[i])
        ax.set_title(day, loc='left', fontsize=12, color=palette[i])
        ax.set_ylabel('')
        ax.set_ylim(0, gym_data[gym_name].max() + 5)  # Add some space at the top of each plot

    # Set labels and titles
    axes[0].set_title(f'Average Attendance per Hour - {gym_name}', fontsize=16)
    axes[-1].set_xlabel('Hour of the Day')

    # Set x-axis major locator to integer and format the x-axis labels to show all hours as ticks
    for ax in axes:
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xticks(range(24))  # Set x-ticks to show every hour
        ax.tick_params(labelsize=10)

    # Remove the vertical gaps between subplots
    plt.subplots_adjust(hspace=0)

    # Remove spines and grid lines
    for ax in axes:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(False)

    # Set the background color of each subplot to match the fill for aesthetics
    for i, ax in enumerate(axes):
        ax.set_facecolor(palette[i] + (0.1,))  # Adjust alpha for background

    # Adjust the layout
    plt.tight_layout()
    plt.show()

# Create filled line plots for each gym
create_filled_line_plots_with_hours(average_attendance, 'GymA')
create_filled_line_plots_with_hours(average_attendance, 'GymB')
create_filled_line_plots_with_hours(average_attendance, 'GymC')
