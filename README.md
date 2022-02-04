# forecast-weather-qa-tests

Tests for commandline app to show tomorrow's forecast using public API: https://www.metaweather.com/api/

Originally used app is here https://github.com/uryuk/forecast-weather-qa

## Notes
* Tests do not affect the way how app is running, originally using args and stdout
* Test setup for each test is done with dependencies of fixtures
* forecast fixture intercept stdout and prevent sys.exit depending on test case
* mock_args fixture allows to parametrize sys.args if needed. If not default param for city fixture is 'Dubai'

## Tests can be launched with command:

```
pytest tests/functional_test.py -s -v 

22 passed in 21.41s
```

### Install dependencies

```
pip install -r requirements.txt
```
