import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Load the dataset
file_path = 'data.csv'  # Replace with your file path
data = pd.read_csv(file_path)

# Convert 'Date' and 'Time' columns to datetime and extract day of the week and hour
data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'], format='%d/%m/%Y %H:%M:%S')
data['Hour'] = data['DateTime'].dt.hour
data['Weekday'] = data['DateTime'].dt.day_name()

# Aggregate gym attendance by hour and day of the week
attendance_by_hour = data.groupby(['Weekday', 'Hour']).agg({'GymA': 'mean', 'GymB': 'mean', 'GymC': 'mean'}).reset_index()

# Filtering out zero attendance data points for the purpose of finding lowest non-zero attendance
non_zero_attendance = attendance_by_hour[(attendance_by_hour['GymA'] > 0) | 
                                         (attendance_by_hour['GymB'] > 0) | 
                                         (attendance_by_hour['GymC'] > 0)]

# Sorting the days in order
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
non_zero_attendance['Weekday'] = pd.Categorical(non_zero_attendance['Weekday'], categories=days_of_week, ordered=True)
non_zero_attendance = non_zero_attendance.sort_values('Weekday')

# Define a more distinctive color palette
palette = sns.color_palette("tab10", n_colors=3)

# Plotting the graphs
fig, axes = plt.subplots(nrows=7, ncols=1, figsize=(15, 28), sharex=False)

for i, day in enumerate(days_of_week):
    ax = axes[i]
    # Plot each gym with a different color
    sns.lineplot(x='Hour', y='GymA', data=non_zero_attendance[non_zero_attendance['Weekday'] == day], ax=ax, color=palette[0], label='GymA')
    sns.lineplot(x='Hour', y='GymB', data=non_zero_attendance[non_zero_attendance['Weekday'] == day], ax=ax, color=palette[1], label='GymB')
    sns.lineplot(x='Hour', y='GymC', data=non_zero_attendance[non_zero_attendance['Weekday'] == day], ax=ax, color=palette[2], label='GymC')

    ax.set_title(f'Gym Attendance on {day}')
    ax.set_ylabel('Average Attendance')
    ax.set_xlabel('Hour of Day')
    ax.set_xticks(np.arange(0, 24, 1))  # Set x-ticks to show every hour

plt.tight_layout()
plt.show()
