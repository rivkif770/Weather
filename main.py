import requests
from flask import Flask, render_template

app = Flask(__name__)

API_KEY = '1b81f9ca443929eb2e7392bb54244b2f4'

def get_data_from_api():
    locations = ['Eilat,IL', 'London,GB', 'New York,US', 'Alaska,US']
    city_translations = {"London": "לונדון", "Eilat": "אילת", "New York": "ניו יורק", "Alaska": "אלסקה"}
    results = []

    for location in locations:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&lang=he&appid={API_KEY}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            city_name = location.split(',')[0]
            city_name_hebrew = city_translations.get(city_name, city_name)
            city_data = {
                "name": city_name_hebrew,
                "description": data['weather'][0]['description'],
                "temp": data['main']['temp'],
                "feels_like": data['main']['feels_like'],
                "humidity": data['main']['humidity'],
                "icon": data['weather'][0]['icon'],
            }
            results.append(city_data)
        except requests.exceptions.RequestException as e:
            results.append({"location": location, "error": str(e)})  # הוסף שגיאה אם יש

    return results

@app.route('/')
def index():
    weather_data = get_data_from_api()
    return render_template('index.html', weather_data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)
