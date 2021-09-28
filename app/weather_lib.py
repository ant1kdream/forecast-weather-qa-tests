import requests
from app.models import Forecast, City


API_CITY_ID_URL = 'https://www.metaweather.com/api/location/search/?query={}'
API_CITY_WEATHER_URL = 'https://www.metaweather.com/api/location/{}/{}'
FORECAST_KEY = 'consolidated_weather'


def get_forecast(city_name, date):
    city = _get_city_by_name(city_name)

    data = _get_weather_by_city_id(city.woeid, date)
    if data is not None and len(data) > 0:
        # get info for the current day
        f = Forecast().from_dict(data[0])
        return f
    else:
        raise AssertionError('Can not grab weather info for {}'.format(city_name))


def _get_city_by_name(city):
    r = requests.get(API_CITY_ID_URL.format(city))

    data = r.json()
    if data:
        # return first result found
        return City().from_dict(r.json()[0])
    else:
        raise LookupError('{} city not found'.format(city))


def _get_weather_by_city_id(city_id, date):
    date_str = date.strftime("%Y/%m/%d")
    r = requests.get(API_CITY_WEATHER_URL.format(city_id, date_str))
    return r.json()
