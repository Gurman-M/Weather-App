from geopy.geocoders import Nominatim
from flask import Flask, render_template, url_for, request
import time
import requests # allows for making HTTP requests

def check_city(city_name):

    # Nominatim allows a maximum of 1 request per second
    time.sleep(1)

    try:
        # calling the Nominatim tool
        location = Nominatim(user_agent="GetLocation")
 
        # entering the location name
        getLocation = location.geocode(city_name)
 
        # makes sure city name is valid
        if (getLocation == None):
            lat = None
            long = None
            return lat, long
        else:
            lat = getLocation.latitude
            long = getLocation.longitude
            return lat, long
    except:
        # city name is invalid
        return False

def kelvin_to_c_f(kelvin):
    c = kelvin - 273.15
    f = c * (9/5) + 32
    return c, f

def weather_request(cityname):
    CITY = cityname

    city_check = check_city(CITY)

    api_file = open("app/api_key.txt", "r")
    API_KEY = api_file.read()
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

    url = BASE_URL + "lat=" + str(city_check[0]) + "&lon=" + str(city_check[1]) + "&appid=" + API_KEY

    if (city_check[0] != None):
        # makes HTTP call to API using url and gets back json
        response = requests.get(url).json()

        general_weather = response['weather'][0]['main']
        temp_k = response['main']['temp']
        temp_c = kelvin_to_c_f(float(temp_k))[0]
        temp_f = kelvin_to_c_f(float(temp_k))[1]
        feelslike_k = response['main']['feels_like']
        feelslike_c = kelvin_to_c_f(float(feelslike_k))[0]
        feelslike_f = kelvin_to_c_f(float(feelslike_k))[1]
        country = response['sys']['country']
        city_location = response['name']

        return f"{temp_c:.2f}" + " °C", f"{temp_f:.2f}" + " °F", f"{feelslike_c:.2f}" + " °C", f"{feelslike_f:.2f}" + " °F", f"{general_weather}", f"{country}", f"{city_location}"
    else:
        return None

    api_file.close()

def main():
    app = Flask(__name__, static_folder='static')

    app.static_folder = 'static'

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/find_weather", methods=["POST", "GET"])
    def find_weather():
        cityname = request.form["cityname"]
        info_list = weather_request(cityname)
        if (info_list == None):
            return render_template("display_weather.html", header_val="The city name you have entered does not exist.")
        else:
            return render_template("display_weather.html", header_val=cityname, c_val=info_list[0], f_val=info_list[1], fl_c=info_list[2], fl_f=info_list[3], weather_gen=info_list[4], cn=info_list[5], city_loc=info_list[6])

    if __name__ == "__main__":
            app.run(debug=True)

main()
