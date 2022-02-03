import datetime
import io
import pytest
from contextlib import redirect_stdout

import app.runner
import test_data


@pytest.fixture(autouse=True, params=[{'city': 'Dubai'}], ids=lambda x: 'Dubai')
def city(request):
    """ Set default city for fixture in case fixture is not parametrized """
    return request.param['city']


@pytest.fixture
def mock_args(monkeypatch, city):
    """ Set mock city for sys.argv """

    monkeypatch.setattr("sys.argv", ["pytest", city])
    yield monkeypatch

    # teardown for mocked city
    monkeypatch.undo()


@pytest.fixture
def forecast(mock_args) -> str:
    """ Get stdout result from app.runner """
    f = io.StringIO()
    try:
        with redirect_stdout(f):
            app.runner.run()
    except SystemExit as e:  # prevent sys from exit
        pass
    # get forecast or error message depending on test case
    result = f.getvalue()
    yield result


def convert_data(forecast) -> dict:
    """ Convert str to dict with data """

    # prevent converting data if city was not found in API
    assert 'city not found' not in forecast, forecast

    result = {}
    forecast = list(filter(None, forecast.split('\n')))  # remove empty elements from list

    try:
        forecast_description = forecast[0]
        weather_state = forecast[1]
        weather_data = forecast[2:]

        result['date'] = forecast_description.split()[1][1:-1].strip()
        result['city'] = forecast_description.split('in')[-1].strip()
        result['weather_state'] = weather_state.strip()

        for data in weather_data:
            split_data = data.split(':')
            param = split_data[0].strip()
            value = split_data[1].strip()
            result[param] = value

    except Exception as e:
        pytest.fail(f'Error in processing {forecast} \nwith next error: {e}')

    return result


@pytest.mark.parametrize('city', ['London', 'San Francisco', 'Rio de Janeiro'])
def test_cities(city, forecast):
    """ Here can be tested different cities (in fact all existing in API)
    for functional test purposes taken 3 cities with different number of words in each """
    result = convert_data(forecast)
    assert city == result['city'], f'{city} is not equal to {result[city]}'


def test_date(forecast):
    """ Test date in output is tomorrow's date """
    result = convert_data(forecast)
    assert 'Tomorrow' in forecast
    assert result['date'] == str(datetime.date.today() + datetime.timedelta(days=1))


@pytest.mark.parametrize('city', ['Toronto', 'Lima', 'Mumbai', 'Moscow', 'Sapporo', 'Melbourne', 'Wellington',
                                  'Oslo', 'Helsinki', 'Lisbon', 'St Petersburg', 'Dubai'])
def test_weather_state(city, forecast):
    """ Positive test for weather state in different locations to cover different states """
    result = convert_data(forecast)
    assert result['weather_state'] in test_data.weather_states, \
        f"{result['weather_state']} is not in {test_data.weather_states}"


def test_weather_params_types(forecast):
    """ Positive test for validation weather params types """
    result = convert_data(forecast)

    assert test_data.degree in result['Temp'], f'{test_data.degree} not in {result["Temp"]}'
    assert test_data.degree in result['Min'], f'{test_data.degree} not in {result["Min"]}'
    assert test_data.degree in result['Max'], f'{test_data.degree} not in {result["Max"]}'
    assert test_data.speed in result['Wind speed'], f'{test_data.speed} not in {result["Wind Speed"]}'
    assert test_data.percent in result['Humidity'], f'{test_data.percent} not in {result["Humidity"]}'
    assert test_data.pressure in result['Air pressure'], f'{test_data.pressure} not in {result["Air pressure"]}'


def test_weather_params_values(forecast):
    """ Positive test for validation weather params values """
    result = convert_data(forecast)
    temp_value = float(result['Temp'].split(test_data.degree)[0].strip())
    min_value = float(result['Min'].split(test_data.degree)[0].strip())
    max_value = float(result['Max'].split(test_data.degree)[0].strip())
    wind_value = float(result['Wind speed'].split(test_data.speed)[0].strip())
    humidity_value = float(result['Humidity'].split(test_data.percent)[0].strip())
    pressure_value = float(result['Air pressure'].split(test_data.pressure)[0].strip())

    assert test_data.earth_min_temp <= temp_value <= test_data.earth_max_temp, f'unexpected {min_value=}'
    assert min_value >= test_data.earth_min_temp, f'unexpected {min_value=}'
    assert max_value <= test_data.earth_max_temp, f'unexpected {min_value=}'
    assert test_data.earth_min_wind_speed <= wind_value <= test_data.earth_max_wind_speed, f'unexpected {wind_value=}'
    assert test_data.earth_min_humidity <= humidity_value <= test_data.earth_max_humidity, f'unexpected {wind_value=}'
    assert test_data.earth_min_pressure <= pressure_value <= test_data.earth_max_pressure, f'unexpected {pressure_value=}'


@pytest.mark.parametrize('city', ['FakeCity', 'FLondon', ' London', 'Ottawa'])
def test_negative_city(city, forecast):
    """ Negative test case for not existing city, city with mistake, city with space, city not in API"""
    assert city in forecast, f'{city} not in forecast'
    assert 'city not found' in forecast, f'error message not displayed in {forecast} '
