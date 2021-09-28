import argparse
import datetime

from app import weather_lib


def run():
    parser = argparse.ArgumentParser(description='Get current weather from CLI',
                                     prog='weather', usage='%(prog)s [city_name]')
    parser.add_argument('city')
    args = parser.parse_args()

    try:
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        print("Tomorrow's ({}) weather in {}\n".format(tomorrow, args.city))
        print(weather_lib.get_forecast(args.city, tomorrow))
    except (LookupError, AssertionError) as e:
        print(e)
        exit(1)
