import pymongo
from datetime import datetime
import json
import httplib2
from methods import thread_for_plotting_forecast_data
from flask import Flask, render_template

# Settings for the OpenWeatherMap API and Folium map
open_weather_map_API_key = "cb432f2c95fd2f39dd447de797422b39"
open_weather_API_endpoint = "http://api.openweathermap.org/"

# Initialized HTTPlib for HTTP requests
http_initializer = httplib2.Http()

# Get city names for which we want to get forecast data from configuration file
city_names =['barrie', 'toronto', 'vancouver']

# How often do we want our app to refresh and download data
refresh_frequency = 60

client = pymongo.MongoClient("mongodb+srv://ilker:Balkeslee97@dataprogramming.t2eef.mongodb.net/?retryWrites=true&w=majority")

    # We create a collection for each city to store data w.r.t. city
for city in city_names:
  url = open_weather_API_endpoint + "/data/2.5/forecast?q=" + city + "&appid=" + open_weather_map_API_key
  http_initializer = httplib2.Http()
  response, content = http_initializer.request(url, 'GET')
  utf_decoded_content = content.decode('utf-8')
  json_object = json.loads(utf_decoded_content)
  print(json_object)
        

        # Creating Mongodb database
  db = client.weather_data

        # Putting Openweathermap API data in database, with timestamp as primary key
  for element in json_object["list"]:
          try:
              datetime = element['dt']
              del element['dt'    ]
              db['{}'.format(city)].insert_one({'_id': datetime, "data": element})
          except pymongo.errors.DuplicateKeyError:
              continue




#a = thread_for_plotting_forecast_data()
#date = a[1]
#datef = [i[5:16] for i in date]
#weatherC = [x-273.15 for x in a[2]]
#weather = [round(num, 1) for num in weatherC]
#result  = [item for sublist in zip(datef, weather) for item in sublist]
#n = 2
#x = [result[i:i + n] for i in range(0, len(result), n)]
#print(x)


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
   return render_template('mline.html')


if __name__ == '__main__':
    app.debug = True
    app.run(debug=True, TEMPLATES_AUTO_RELOAD = True)