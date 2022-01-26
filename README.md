# forecast-weather-qa

Imagine you have a commandline app to show tomorrow's forecast using public API: https://www.metaweather.com/api/

Sample output:

```
python weather.py dubai

Tomorrow's (2021-09-29) weather in Dubai

Light Cloud 
Temp: 35.03 °C
Min: 29.87 °C
Max: 35.84 °C
Wind speed: 6.7 m/s
Humidity: 59 %
Air pressure: 1005.0 mbar

```

## Task 
* How will you test the app? Write several automated tests to prove the correct work of application.
* Ideally, tests should not touch the real service and work without the Internet.
* Bonus task. Create CI pipeline with GitHub Actions or any alternative.

### Install dependencies

```
pip install -r requirements.txt
```
