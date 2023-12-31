import requests

api_key = "1e0c79c1fcc9444ca23110614231012"

def get_weather_data_daily(latitude, longitude):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={latitude},{longitude}"

    data = requests.get(url)
    response = data.json()

    if data.status_code == 200:
        location_name = "Location: " + response["location"]["name"] + ", " + response["location"]["region"]
        last_update = "Last Updated: " + str(response["current"]["last_updated"])
        temp = int(response["current"]["temp_c"])
        feels_like = response["current"]["feelslike_c"]
        temperature = f"Temperature: {temp}°C, Feels like: {feels_like}°C"
        condition = "Condition: " + response["current"]["condition"]["text"]
        wind = "Wind: " + str(response["current"]["wind_kph"]) + "km/h"
        humidity = "Humidity: " + str(response["current"]["humidity"]) + "%"

        great_text = f"{location_name}\n{last_update}\n{temperature}\n{condition}\n{wind}\n{humidity}"

        return great_text  
    else:
        return None
    
def get_weather_data_weekly(latitude, longitude):
    date1 = "2023-12-10"
    date2 = "2023-12-17"
    url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={latitude},{longitude}&days=7"

    data = requests.get(url)
    response = data.json()

    if data.status_code == 200:
        result = ""
        for day in response["forecast"]["forecastday"]:
            date = day["date"]
            avg_temp = day["day"]["avgtemp_c"]
            condition = day["day"]["condition"]["text"]
            result += f"{date}: {avg_temp}°C Condition: {condition}\n"
        return result
        # print(str(response["forecast"]["forecastday"][0]["date"]) + ": " + str(response["forecast"]["forecastday"][0]["day"]["avgtemp_c"]) + "°C")
    else:
        return None

# print(get_weather_data_daily(40.95073,71.431896))
# print(get_weather_data_weekly(40.95073,71.431896))