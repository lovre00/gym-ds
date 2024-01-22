# Let's first read the CSV file and calculate the total attendance for each entry.

import pandas as pd



# Load the CSV file to examine its contents

file_path = 'data.csv'

data = pd.read_csv(file_path)



# Calculate the total attendance for each entry

data['Total_Attendance'] = data['GymA'] + data['GymB'] + data['GymC']



# Display the total attendance for each entry

total_attendance_per_entry = data['Total_Attendance'].tolist()

print(total_attendance_per_entry)