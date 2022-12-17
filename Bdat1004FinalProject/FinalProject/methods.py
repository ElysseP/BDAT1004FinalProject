import pymongo
import requests


city_names =['barrie', 'toronto', 'vancouver']

def thread_for_plotting_forecast_data():
    temperature_data_timestamps = []
    temperatures = {}
    date_times = []
    first_time = True
    # Initialize MongoDB client running on localhost
    client = pymongo.MongoClient("mongodb+srv://ilker:Balkeslee97@dataprogramming.t2eef.mongodb.net/?retryWrites=true&w=majority")

    for city in city_names:
        temperatures[city] = []
    # Get all temperature data w.r.t. date and time from database
    with client:
        db = client.weather_data
        for city in city_names:
            data = db['{}'.format(city)].find({})
            for record in data:
                temperatures[city].append(record["data"]["main"]["temp"])
                if first_time:
                    date_times.append(record["data"]["dt_txt"])
            first_time = False
        return (city, date_times, temperatures[city])


    
# Use this thread to download 5 days / 3 hour forecast. Also show alert if there is rain/snow or freeezing temperatures (<2 farenheit) in any of forecast period
def thread_for_5_days_3_hour_forecast():
    '''
    In this method, we download the 5 days and 3 hour separated data and store it in
    the mongodb database making timestamp as primary key, thus preventing duplicates

    '''
    # Initialize MongoDB client running on localhost