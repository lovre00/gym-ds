import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('data.csv')  # Replace with your file path

# Selecting relevant columns for correlation
correlation_data = data[['GymA', 'GymB', 'GymC', 'temperature', 'relative_humidity', 
                         'apparent_temperature', 'precipitation', 'rain', 'showers', 
                         'snowfall', 'weather_code', 'cloud_cover', 'wind_speed']]

# Calculate the correlation matrix
corr_matrix = correlation_data.corr()

# Plotting the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Correlation between Gym Attendance and Weather Conditions")
plt.show()
