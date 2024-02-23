import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import datetime
import requests
from scraper import get_stats

def info(message):
    print(f"[  INFO  ]\t{message}")

# Load the data
info("Reading CSV file...")
df = pd.read_csv('data.csv')

# Preprocessing
# Convert 'Day' to categorical
info("Preprocessing data...")
df[(df['GymA'] != 0) | (df['GymB'] != 0) | (df['GymC'] != 0)]
df['Day'] = pd.Categorical(df['Day'])
df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d/%m/%Y %H:%M:%S')
df['Hour'] = df['DateTime'].dt.hour
df['Month'] = df['DateTime'].dt.month
df['Weekday'] = df['DateTime'].dt.weekday  # Monday=0, Sunday=6

# Drop original date, time, and datetime columns
df.drop(['Date', 'Time', 'DateTime'], axis=1, inplace=True)

# Feature and target columns
feature_cols = ['temperature', 'relative_humidity', 'apparent_temperature', 'precipitation', 
                'rain', 'showers', 'snowfall', 'weather_code', 'cloud_cover', 
                'wind_speed', 'Hour', 'Month', 'Weekday']
target_cols = ['GymA', 'GymB', 'GymC']

info("Splitting dataset...")
# Splitting the data into features (X) and targets (y)
X = df[feature_cols]
y = df[target_cols]

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Training the model
info("Training the model...")
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

info("Evaluating the model...")
# Evaluating the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

def get_weather_forecast(latitude, longitude):
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    current_hour = now.hour

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,precipitation,weathercode,cloudcover,windspeed_10m"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error fetching data from Open-Meteo: {response.status_code}")

    data = response.json()

    forecast = data['hourly']
    current_weather = {
        'temperature': forecast['temperature_2m'][current_hour],
        'relative_humidity': forecast['relativehumidity_2m'][current_hour],
        'precipitation': forecast['precipitation'][current_hour],
        'weather_code': forecast['weathercode'][current_hour],
        'cloud_cover': forecast['cloudcover'][current_hour],
        'wind_speed': forecast['windspeed_10m'][current_hour],
        # Add default values for 'rain', 'showers', 'snowfall'
        'rain': 0,
        'showers': 0,
        'snowfall': 0,
        'Hour': current_hour,
        'Month': now.month,
        'Weekday': now.weekday()
    }
    

    return current_weather

latitude = 43.5089 
longitude = 16.439
hour = 19
month = datetime.datetime.now().month
weekday = datetime.datetime.now().weekday()

def predict_gym_attendance(forecast_data):
    required_features = ['temperature', 'relative_humidity', 'apparent_temperature', 
                         'precipitation', 'rain', 'showers', 'snowfall', 
                         'weather_code', 'cloud_cover', 'wind_speed', 
                         'Hour', 'Month', 'Weekday']

    forecast_df = pd.DataFrame(columns=required_features)

    for feature in required_features:
        if feature in forecast_data:
            forecast_df.at[0, feature] = forecast_data[feature]
        else:
            forecast_df.at[0, feature] = 0

    predicted_attendance = model.predict(forecast_df)
    return predicted_attendance

info("Getting current weather...")
forecast_data = get_weather_forecast(latitude, longitude)

info("Making a prediction...")
attendance_prediction = predict_gym_attendance(forecast_data)

gym_a_predicted = round(attendance_prediction[0][0])
gym_b_predicted = round(attendance_prediction[0][1])
gym_c_predicted = round(attendance_prediction[0][2])

info("Scraping actual data...")
actual_data = get_stats()

for i in range(0, 3):
    actual_data[i] = int(actual_data[i].replace(" members", ""))

info("Done!")
print()

for i in range(0, 3):
    temp = round(attendance_prediction[0][i])
    width = int(max(temp, actual_data[i]))
    print(f"\t\tLocation {i} predicted:\t{temp}\t" + "[" + "*" * temp + " " * (width - temp) + "]")
    print(f"\t\tLocation {i} actual:\t{actual_data[i]}\t" + "[" + "*" * actual_data[i] + " " * (width - actual_data[i]) + "]")
    print()
