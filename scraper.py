from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import openmeteo_requests
import requests_cache
from retry_requests import retry
import time
from datetime import datetime
import schedule
from powermanagement import long_running
import json


def get_credentials():
    with open("login.json", "r") as file:
        return json.load(file)

def get_weather():
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 43.5089,
	    "longitude": 16.4392,
	    "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "precipitation", "rain", "showers", "snowfall", "weather_code", "cloud_cover", "wind_speed_10m"],
	    "hourly": "uv_index"
    }
    
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    current = response.Current()
    
    return current

def get_stats():
    url = 'https://marjan.split-fitness.club/admin/signin'

    # set Firefox options
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    gym_a = None
    gym_b = None
    gym_c = None

    login = get_credentials()

    try:
        browser = webdriver.Firefox(options=options)
        browser.get(url)

        # fill email and pass and click submit
        email = browser.find_element(By.NAME, "email")
        password = browser.find_element(By.NAME, "password")

        email.clear()
        email.send_keys(login['username'])

        password.clear()
        password.send_keys(login['password'])

        browser.find_element(By.XPATH, "//button[@class='btn btn-dark btn-block']").click()

        time.sleep(3)
    
        modal = browser.find_element(By.ID, "openModal44")
        browser.execute_script("arguments[0].click()", modal)

        time.sleep(1)
        
        gym_a = browser.find_element(By.ID, "battery1").text
        gym_b = browser.find_element(By.ID, "battery2").text
        gym_c = browser.find_element(By.ID, "battery3").text
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")

    return [gym_a, gym_b, gym_c]

def log_data(data):
    current_time = datetime.now().strftime("%A %d/%m/%Y %H:%M:%S")

    gym_a = data[0].replace(' members', '')
    gym_b = data[1].replace(' members', '')
    gym_c = data[2].replace(' members', '')

    current = get_weather()

    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_apparent_temperature = current.Variables(2).Value()
    current_precipitation = current.Variables(3).Value()
    current_rain = current.Variables(4).Value()
    current_showers = current.Variables(5).Value()
    current_snowfall = current.Variables(6).Value()
    current_weather_code = current.Variables(7).Value()
    current_cloud_cover = current.Variables(8).Value()
    current_wind_speed_10m = current.Variables(9).Value()

    with open('data.csv', 'a') as log_file:
        log_file.write(f"{current_time} {gym_a} {gym_b} {gym_c} {current_temperature_2m} {current_relative_humidity_2m} {current_apparent_temperature} {current_precipitation} {current_rain} {current_showers} {current_snowfall} {current_weather_code} {current_cloud_cover} {current_wind_speed_10m}\n")

    return current_time

def print_stats(data):
    print("----------------------------")
    print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("............................")
    print("\tSplit 3 : " + data[0])
    print("\tLokve   : " + data[1])
    print("\tGripe   : " + data[2])
    print("----------------------------")
    get_weather()

def job():
    data = get_stats()
    log_data(data)
    print_stats(data)

@long_running
def main():
    job()
    schedule.every(30).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()



